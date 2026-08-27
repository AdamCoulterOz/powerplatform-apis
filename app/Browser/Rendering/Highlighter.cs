using System.Text;

namespace PowerPlatformApis.Browser.Rendering;

/// <summary>
/// Small syntax highlighters that emit the keel code-block token classes
/// (c comment, k keyword, s string, n number, t type, f function), so colour
/// comes from the design system's own tokens in both themes. Writing this in
/// C# rather than binding a JS highlighter is what keeps the palette ours:
/// the alternative was overriding someone else's light-mode theme after the
/// fact.
/// </summary>
public static class Highlighter
{
    public static string Json(string json)
    {
        var sb = new StringBuilder(json.Length + 64);
        var i = 0;
        while (i < json.Length)
        {
            var c = json[i];

            if (c == '"')
            {
                var start = i;
                i++;
                while (i < json.Length)
                {
                    if (json[i] == '\\') { i += 2; continue; }
                    if (json[i] == '"') { i++; break; }
                    i++;
                }
                var text = json[start..Math.Min(i, json.Length)];
                // a string followed by a colon is a property name
                var j = i;
                while (j < json.Length && char.IsWhiteSpace(json[j])) j++;
                var cls = j < json.Length && json[j] == ':' ? "t" : "s";
                Span(sb, cls, text);
                continue;
            }

            if (char.IsDigit(c) || (c == '-' && i + 1 < json.Length && char.IsDigit(json[i + 1])))
            {
                var start = i;
                while (i < json.Length && (char.IsDigit(json[i]) || json[i] is '.' or 'e' or 'E' or '+' or '-')) i++;
                Span(sb, "n", json[start..i]);
                continue;
            }

            foreach (var lit in Literals)
            {
                if (i + lit.Length <= json.Length && string.CompareOrdinal(json, i, lit, 0, lit.Length) == 0)
                {
                    Span(sb, "k", lit);
                    i += lit.Length;
                    goto next;
                }
            }

            Escape(sb, c);
            i++;
        next: ;
        }
        return sb.ToString();
    }

    private static readonly string[] Literals = { "true", "false", "null" };

    public static string Shell(string text)
    {
        var sb = new StringBuilder(text.Length + 64);
        foreach (var rawLine in text.Split('\n'))
        {
            var line = rawLine;
            if (line.TrimStart().StartsWith('#'))
            {
                Span(sb, "c", line);
                sb.Append('\n');
                continue;
            }

            var i = 0;
            var first = true;
            while (i < line.Length)
            {
                var c = line[i];

                if (c is '\'' or '"')
                {
                    var quote = c;
                    var start = i;
                    i++;
                    while (i < line.Length && line[i] != quote) i++;
                    if (i < line.Length) i++;
                    Span(sb, "s", line[start..i]);
                    continue;
                }

                if (char.IsWhiteSpace(c)) { Escape(sb, c); i++; continue; }

                var wordStart = i;
                while (i < line.Length && !char.IsWhiteSpace(line[i]) && line[i] is not '\'' and not '"') i++;
                var word = line[wordStart..i];

                if (word.StartsWith('-')) Span(sb, "k", word);
                else if (first) Span(sb, "f", word);
                else Escape(sb, word);
                first = false;
            }
            sb.Append('\n');
        }
        return sb.ToString().TrimEnd('\n');
    }

    private static void Span(StringBuilder sb, string cls, string text)
    {
        sb.Append("<span class=\"").Append(cls).Append("\">");
        Escape(sb, text);
        sb.Append("</span>");
    }

    private static void Escape(StringBuilder sb, string text)
    {
        foreach (var c in text) Escape(sb, c);
    }

    private static void Escape(StringBuilder sb, char c)
    {
        switch (c)
        {
            case '&': sb.Append("&amp;"); break;
            case '<': sb.Append("&lt;"); break;
            case '>': sb.Append("&gt;"); break;
            default: sb.Append(c); break;
        }
    }
}
