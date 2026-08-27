using System.Text.Json;

namespace PowerPlatformApis.Browser.Model;

/// <summary>
/// One node of a schema tree. A node may be a `$ref` to a named component, in
/// which case <see cref="Target"/> resolves it lazily: schemas here are
/// genuinely cyclic (a model can reference itself through a property), so the
/// renderer walks with a visited set rather than eagerly expanding.
/// </summary>
public sealed class SchemaRef
{
    private readonly JsonElement _e;
    private readonly OpenApiSpec _spec;
    private SchemaRef? _resolved;
    private bool _resolvedOnce;

    public SchemaRef(JsonElement e, OpenApiSpec spec)
    {
        _e = e;
        _spec = spec;
        Reference = OpenApiSpec.Str(e, "$ref");
    }

    /// <summary>The `$ref` string, when this node is a reference.</summary>
    public string? Reference { get; }

    /// <summary>Component name when this node is a reference, else null.</summary>
    public string? RefName => Reference is null ? null : OpenApiSpec.SchemaName(Reference);

    /// <summary>The referenced schema, or this node when it is inline.</summary>
    public SchemaRef Target
    {
        get
        {
            if (Reference is null) return this;
            if (!_resolvedOnce)
            {
                _resolvedOnce = true;
                _resolved = _spec.Resolve(Reference);
            }
            return _resolved ?? this;
        }
    }

    public string? Type => OpenApiSpec.Str(_e, "type");
    public string? Format => OpenApiSpec.Str(_e, "format");
    public string? Description => OpenApiSpec.Str(_e, "description");
    public bool IsStub => OpenApiSpec.Bool(_e, "x-stub");
    public bool Nullable => OpenApiSpec.Bool(_e, "nullable");
    public IReadOnlyList<string> Notes => OpenApiSpec.StrArr(_e, "x-notes");
    public IReadOnlyList<string> Enum => OpenApiSpec.Arr(_e, "enum")
        .Select(v => v.ValueKind == JsonValueKind.String ? v.GetString()! : v.ToString())
        .ToList();

    /// <summary>Microsoft's extensible-enum marker: the listed values are known, not exhaustive.</summary>
    public bool EnumIsOpen =>
        OpenApiSpec.Obj(_e, "x-ms-enum") is { } x && OpenApiSpec.Bool(x, "modelAsString");

    public SchemaRef? Items =>
        _e.ValueKind == JsonValueKind.Object && _e.TryGetProperty("items", out var i) ? new SchemaRef(i, _spec) : null;

    public SchemaRef? AdditionalProperties =>
        _e.ValueKind == JsonValueKind.Object
        && _e.TryGetProperty("additionalProperties", out var a)
        && a.ValueKind == JsonValueKind.Object
            ? new SchemaRef(a, _spec) : null;

    public IReadOnlyList<SchemaRef> AllOf => Composite("allOf");
    public IReadOnlyList<SchemaRef> OneOf => Composite("oneOf");
    public IReadOnlyList<SchemaRef> AnyOf => Composite("anyOf");

    private IReadOnlyList<SchemaRef> Composite(string name) =>
        OpenApiSpec.Arr(_e, name).Select(x => new SchemaRef(x, _spec)).ToList();

    private HashSet<string> RequiredSet =>
        OpenApiSpec.StrArr(_e, "required").ToHashSet(StringComparer.Ordinal);

    /// <summary>Properties in document order, with their required flag.</summary>
    public IReadOnlyList<SchemaProperty> Properties
    {
        get
        {
            if (OpenApiSpec.Obj(_e, "properties") is not { } props) return Array.Empty<SchemaProperty>();
            var required = RequiredSet;
            return props.EnumerateObject()
                .Select(p => new SchemaProperty(p.Name, new SchemaRef(p.Value, _spec), required.Contains(p.Name)))
                .ToList();
        }
    }

    /// <summary>
    /// A description carried alongside a `$ref` has to be expressed as
    /// `allOf: [ $ref ]` + description, since OpenAPI 3.0 forbids siblings of
    /// `$ref`. Unwrap that shape so the renderer sees one node.
    /// </summary>
    public SchemaRef Unwrapped
    {
        get
        {
            var all = AllOf;
            if (all.Count == 1 && Properties.Count == 0 && Type is null) return all[0];
            return this;
        }
    }

    /// <summary>Short type label for a property row, e.g. `string`, `string&lt;uuid&gt;`, `RoleDefinition[]`.</summary>
    public string TypeLabel
    {
        get
        {
            var node = Unwrapped;
            if (node.RefName is { } rn) return rn;

            var t = node.Type;
            if (t == "array")
            {
                var item = node.Items?.Unwrapped;
                if (item is null) return "array";
                var inner = item.RefName ?? item.Type ?? "object";
                return $"{inner}[]";
            }
            if (node.AdditionalProperties is { } ap)
            {
                var v = ap.Unwrapped;
                return $"map<string, {v.RefName ?? v.Type ?? "object"}>";
            }
            if (node.Enum.Count > 0) return t ?? "enum";
            if (t is null)
            {
                if (node.OneOf.Count > 0) return "oneOf";
                if (node.AnyOf.Count > 0) return "anyOf";
                if (node.AllOf.Count > 0) return "allOf";
                return "object";
            }
            return node.Format is { } f ? $"{t}<{f}>" : t;
        }
    }

    /// <summary>True when this node has children worth expanding.</summary>
    public bool IsExpandable
    {
        get
        {
            var node = Unwrapped;
            var target = node.Target;
            if (target.Properties.Count > 0) return true;
            if (target.AdditionalProperties is not null) return true;
            if (target.Items is { } i)
            {
                var it = i.Unwrapped.Target;
                return it.Properties.Count > 0 || it.AdditionalProperties is not null || it.Enum.Count > 0;
            }
            return target.OneOf.Count > 0 || target.AnyOf.Count > 0 || target.AllOf.Count > 0;
        }
    }

    /// <summary>Constraint chips shown next to a property, e.g. `minLength: 3`.</summary>
    public IEnumerable<string> Constraints
    {
        get
        {
            foreach (var key in new[] { "minLength", "maxLength", "minimum", "maximum", "pattern", "default" })
            {
                if (_e.ValueKind != JsonValueKind.Object || !_e.TryGetProperty(key, out var v)) continue;
                var text = v.ValueKind == JsonValueKind.String ? v.GetString() : v.ToString();
                if (!string.IsNullOrEmpty(text)) yield return $"{key}: {text}";
            }
        }
    }

    /// <summary>A JSON example generated from the schema, used for the sample panes.</summary>
    public JsonElement? Example => null;

    internal JsonElement Raw => _e;
}

public sealed record SchemaProperty(string Name, SchemaRef Schema, bool Required);
