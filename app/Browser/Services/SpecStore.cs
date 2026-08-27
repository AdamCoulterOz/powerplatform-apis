using System.Net.Http.Json;
using System.Text.Json.Serialization;
using PowerPlatformApis.Browser.Model;

namespace PowerPlatformApis.Browser.Services;

/// <summary>One entry of the repository's specs.json.</summary>
public sealed class SpecEntry
{
    [JsonPropertyName("id")] public string Id { get; set; } = "";
    [JsonPropertyName("title")] public string Title { get; set; } = "";
    [JsonPropertyName("url")] public string Url { get; set; } = "";
    [JsonPropertyName("repo")] public string Repo { get; set; } = "";
}

/// <summary>
/// Loads the spec catalogue and the specs themselves. Parsed specs are cached
/// for the session: they are static files and re-parsing a 350-schema document
/// on every navigation would be wasteful.
/// </summary>
public sealed class SpecStore(HttpClient http)
{
    private readonly Dictionary<string, OpenApiSpec> _cache = new(StringComparer.Ordinal);

    // The app is the site: specs.json and the specs it points at sit beside
    // index.html, so paths resolve against the base href with no prefix.
    private const string SiteRoot = "";

    public IReadOnlyList<SpecEntry> Catalogue { get; private set; } = Array.Empty<SpecEntry>();

    public async Task<IReadOnlyList<SpecEntry>> LoadCatalogueAsync()
    {
        if (Catalogue.Count > 0) return Catalogue;
        Catalogue = await http.GetFromJsonAsync<List<SpecEntry>>(SiteRoot + "specs.json") ?? new List<SpecEntry>();
        return Catalogue;
    }

    public async Task<OpenApiSpec> LoadSpecAsync(SpecEntry entry)
    {
        if (_cache.TryGetValue(entry.Id, out var cached)) return cached;
        var json = await http.GetStringAsync(SiteRoot + entry.Url);
        var spec = OpenApiSpec.Parse(json);
        _cache[entry.Id] = spec;
        return spec;
    }
}
