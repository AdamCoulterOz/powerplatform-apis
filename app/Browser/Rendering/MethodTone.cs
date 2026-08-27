using Keel.Components;

namespace PowerPlatformApis.Browser.Rendering;

/// <summary>
/// The HTTP verb as a keel tone. keel draws the marker; which verb is which
/// colour is this app's domain knowledge, so the map lives here and nowhere
/// else. Every site that shows a verb reads it from this one method, so the
/// sidebar, the resource listing and the request line cannot drift apart.
///
/// The verbs are a closed set with conventional colours people already read,
/// and the four that have an obvious semantic home take it: a GET is safe, a
/// POST is the informational primary act, a PUT replaces and a DELETE removes.
/// PATCH has no such home. It takes New because the app needs five verbs to be
/// tellable apart at a glance and New is the remaining distinct step on the
/// scale, not because a PATCH is new. Everything else is unremarkable and grey.
/// </summary>
public static class MethodTone
{
    public static Tone For(string method) => method.ToUpperInvariant() switch
    {
        "GET" => Tone.Good,
        "POST" => Tone.Info,
        "PUT" => Tone.Warning,
        "DELETE" => Tone.Bad,
        "PATCH" => Tone.New,
        _ => Tone.Neutral,
    };
}
