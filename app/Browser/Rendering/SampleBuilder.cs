using System.Text;
using PowerPlatformApis.Browser.Model;

namespace PowerPlatformApis.Browser.Rendering;

/// <summary>Builds the request and response samples shown beside an operation.</summary>
public static class SampleBuilder
{
    private const int MaxDepth = 6;

    public static string Json(SchemaRef? schema)
    {
        if (schema is null) return "{}";
        var sb = new StringBuilder();
        Write(sb, schema, 0, new HashSet<string>(StringComparer.Ordinal));
        return sb.ToString();
    }

    private static void Write(StringBuilder sb, SchemaRef node, int depth, HashSet<string> seen)
    {
        var s = node.Unwrapped;
        var name = s.RefName;
        var target = s.Target;

        // cycle guard: a model can reference itself through a property
        if (name is not null && !seen.Add(name))
        {
            sb.Append('"').Append(name).Append(" { … }\"");
            return;
        }
        if (depth > MaxDepth) { sb.Append("\"…\""); return; }

        try
        {
            if (target.Enum.Count > 0) { sb.Append('"').Append(target.Enum[0]).Append('"'); return; }

            var type = target.Type;

            if (type == "array" || target.Items is not null)
            {
                sb.Append("[\n");
                Indent(sb, depth + 1);
                if (target.Items is { } item) Write(sb, item, depth + 1, seen);
                else sb.Append("\"…\"");
                sb.Append('\n');
                Indent(sb, depth);
                sb.Append(']');
                return;
            }

            var props = target.Properties;
            if (props.Count > 0 || target.AdditionalProperties is not null || type == "object")
            {
                sb.Append("{\n");
                var written = 0;
                foreach (var p in props)
                {
                    if (written > 0) sb.Append(",\n");
                    Indent(sb, depth + 1);
                    sb.Append('"').Append(p.Name).Append("\": ");
                    Write(sb, p.Schema, depth + 1, seen);
                    written++;
                }
                if (props.Count == 0 && target.AdditionalProperties is { } ap)
                {
                    Indent(sb, depth + 1);
                    sb.Append("\"key\": ");
                    Write(sb, ap, depth + 1, seen);
                    written++;
                }
                if (written > 0) sb.Append('\n');
                Indent(sb, depth);
                sb.Append('}');
                return;
            }

            sb.Append(Scalar(type, target.Format));
        }
        finally
        {
            if (name is not null) seen.Remove(name);
        }
    }

    private static string Scalar(string? type, string? format) => type switch
    {
        "integer" => "0",
        "number" => "0",
        "boolean" => "true",
        _ => format switch
        {
            "uuid" => "\"00000000-0000-0000-0000-000000000000\"",
            "date-time" => "\"2026-01-01T00:00:00Z\"",
            "uri" => "\"https://…\"",
            "binary" => "\"<binary>\"",
            _ => "\"string\""
        }
    };

    private static void Indent(StringBuilder sb, int depth) => sb.Append(' ', depth * 2);

    /// <summary>A runnable curl for the operation, with path and query placeholders in place.</summary>
    public static string Curl(Operation op, string server)
    {
        var sb = new StringBuilder();
        var query = op.Parameters
            .Where(p => p.In == "query")
            .Select(p => $"{p.Name}={Placeholder(p)}")
            .ToList();

        var url = server + op.Path + (query.Count > 0 ? "?" + string.Join("&", query) : "");

        sb.Append("curl --request ").Append(op.Method).Append(" \\\n");
        sb.Append("  --url '").Append(url).Append("' \\\n");
        sb.Append("  --header 'Authorization: Bearer $TOKEN'");

        if (op.RequestBody is { Schema: { } schema })
        {
            sb.Append(" \\\n  --header 'Content-Type: application/json' \\\n");
            sb.Append("  --data '").Append(Json(schema)).Append('\'');
        }
        return sb.ToString();
    }

    private static string Placeholder(Parameter p)
    {
        var d = p.Schema?.Target;
        if (d is not null && d.Enum.Count > 0) return d.Enum[0];
        if (d?.Raw.ValueKind == System.Text.Json.JsonValueKind.Object
            && d.Raw.TryGetProperty("default", out var def))
        {
            var text = def.ValueKind == System.Text.Json.JsonValueKind.String ? def.GetString() : def.ToString();
            if (!string.IsNullOrEmpty(text)) return text!;
        }
        return "{" + p.Name + "}";
    }
}
