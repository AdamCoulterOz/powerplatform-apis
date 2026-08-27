using System.Text;

namespace PowerPlatformApis.Browser.Rendering;

/// <summary>
/// Syntax highlighting that emits keel's code-block token classes
/// (c comment, k keyword, s string, n number, t type, f function), so colour
/// comes from the design system's own --cb-* variables in both themes.
/// Writing this in C# rather than binding a JS highlighter is what keeps the
/// palette ours: the alternative is overriding someone else's light-mode theme
/// after the fact.
/// </summary>
public static class Highlighter
{
    public static string Highlight(string code, CodeLanguage language) => language switch
    {
        CodeLanguage.Json => Json(code),
        CodeLanguage.Bash => Bash(code),
        CodeLanguage.Http => Http(code),
        CodeLanguage.CSharp => Keywords(code, CSharpKeywords, CSharpTypes),
        CodeLanguage.Xml => Xml(code),
        CodeLanguage.Yaml => Yaml(code),
        _ => Plain(code)
    };

    // ------------------------------------------------------------------ JSON

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
                i = SkipString(json, i);
                var text = json[start..i];
                var j = i;
                while (j < json.Length && char.IsWhiteSpace(json[j])) j++;
                // a string followed by a colon is a property name
                Span(sb, j < json.Length && json[j] == ':' ? "t" : "s", text);
                continue;
            }

            if (IsNumberStart(json, i))
            {
                var start = i;
                i = SkipNumber(json, i);
                Span(sb, "n", json[start..i]);
                continue;
            }

            if (TryLiteral(json, ref i, sb, JsonLiterals)) continue;

            Escape(sb, c);
            i++;
        }
        return sb.ToString();
    }

    private static readonly string[] JsonLiterals = { "true", "false", "null" };

    // ------------------------------------------------------------------ Bash

    public static string Bash(string text)
    {
        var sb = new StringBuilder(text.Length + 64);
        var lines = text.Split('\n');
        for (var li = 0; li < lines.Length; li++)
        {
            var line = lines[li];
            if (line.TrimStart().StartsWith('#'))
            {
                Span(sb, "c", line);
                if (li < lines.Length - 1) sb.Append('\n');
                continue;
            }

            var i = 0;
            var atCommand = true;
            while (i < line.Length)
            {
                var c = line[i];

                if (c is '\'' or '"')
                {
                    var start = i;
                    i = SkipQuoted(line, i);
                    Span(sb, "s", line[start..i]);
                    continue;
                }

                if (c == '$')
                {
                    var start = i;
                    i++;
                    if (i < line.Length && line[i] == '{') { while (i < line.Length && line[i] != '}') i++; if (i < line.Length) i++; }
                    else while (i < line.Length && (char.IsLetterOrDigit(line[i]) || line[i] == '_')) i++;
                    Span(sb, "n", line[start..i]);
                    continue;
                }

                if (char.IsWhiteSpace(c)) { Escape(sb, c); i++; continue; }

                var wordStart = i;
                while (i < line.Length && !char.IsWhiteSpace(line[i]) && line[i] is not '\'' and not '"' and not '$') i++;
                var word = line[wordStart..i];

                if (word.StartsWith('-')) Span(sb, "k", word);
                else if (word is "|" or "&&" or "||" or ";" or "\\") Escape(sb, word);
                else if (atCommand) { Span(sb, "f", word); atCommand = false; }
                else Escape(sb, word);

                if (word is "|" or "&&" or "||" or ";") atCommand = true;
            }
            if (li < lines.Length - 1) sb.Append('\n');
        }
        return sb.ToString();
    }

    // ------------------------------------------------------------------ HTTP

    private static readonly string[] HttpMethods =
        { "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE" };

    public static string Http(string text)
    {
        var sb = new StringBuilder(text.Length + 64);
        var lines = text.Split('\n');
        for (var li = 0; li < lines.Length; li++)
        {
            var line = lines[li];

            if (li == 0 && HttpMethods.Any(m => line.StartsWith(m + " ", StringComparison.Ordinal)))
            {
                var sp = line.IndexOf(' ');
                Span(sb, "f", line[..sp]);
                Escape(sb, line[sp..]);
            }
            else if (line.IndexOf(':') is var colon and > 0 && !line.StartsWith(' '))
            {
                Span(sb, "t", line[..colon]);
                Escape(sb, ":");
                Span(sb, "s", line[(colon + 1)..]);
            }
            else
            {
                Escape(sb, line);
            }
            if (li < lines.Length - 1) sb.Append('\n');
        }
        return sb.ToString();
    }

    // -------------------------------------------------------------- keyword

    private static readonly HashSet<string> CSharpKeywords = new(StringComparer.Ordinal)
    {
        "abstract","as","async","await","base","bool","break","case","catch","class","const","continue",
        "default","do","else","enum","event","false","finally","for","foreach","get","if","in","init",
        "interface","internal","is","namespace","new","null","out","override","params","private",
        "protected","public","readonly","record","ref","return","sealed","set","static","struct",
        "switch","this","throw","true","try","typeof","using","var","virtual","void","when","where","while","yield"
    };

    private static readonly HashSet<string> CSharpTypes = new(StringComparer.Ordinal)
    {
        "byte","char","decimal","double","float","int","long","object","sbyte","short","string",
        "uint","ulong","ushort","Task","List","Dictionary","IEnumerable","Span"
    };

    private static string Keywords(string text, HashSet<string> keywords, HashSet<string> types)
    {
        var sb = new StringBuilder(text.Length + 64);
        var i = 0;
        while (i < text.Length)
        {
            var c = text[i];

            if (c == '/' && i + 1 < text.Length && text[i + 1] == '/')
            {
                var end = text.IndexOf('\n', i);
                if (end < 0) end = text.Length;
                Span(sb, "c", text[i..end]);
                i = end;
                continue;
            }

            if (c is '"' or '\'')
            {
                var start = i;
                i = SkipQuoted(text, i);
                Span(sb, "s", text[start..i]);
                continue;
            }

            if (IsNumberStart(text, i))
            {
                var start = i;
                i = SkipNumber(text, i);
                Span(sb, "n", text[start..i]);
                continue;
            }

            if (char.IsLetter(c) || c == '_')
            {
                var start = i;
                while (i < text.Length && (char.IsLetterOrDigit(text[i]) || text[i] == '_')) i++;
                var word = text[start..i];
                if (keywords.Contains(word)) Span(sb, "k", word);
                else if (types.Contains(word)) Span(sb, "t", word);
                else if (i < text.Length && text[i] == '(') Span(sb, "f", word);
                else Escape(sb, word);
                continue;
            }

            Escape(sb, c);
            i++;
        }
        return sb.ToString();
    }

    // ------------------------------------------------------------- XML, YAML

    public static string Xml(string text)
    {
        var sb = new StringBuilder(text.Length + 64);
        var i = 0;
        while (i < text.Length)
        {
            if (text[i] == '<')
            {
                var end = text.IndexOf('>', i);
                if (end < 0) end = text.Length - 1;
                var tag = text[i..(end + 1)];
                if (tag.StartsWith("<!--", StringComparison.Ordinal)) Span(sb, "c", tag);
                else Span(sb, "t", tag);
                i = end + 1;
                continue;
            }
            Escape(sb, text[i]);
            i++;
        }
        return sb.ToString();
    }

    public static string Yaml(string text)
    {
        var sb = new StringBuilder(text.Length + 64);
        var lines = text.Split('\n');
        for (var li = 0; li < lines.Length; li++)
        {
            var line = lines[li];
            var trimmed = line.TrimStart();

            if (trimmed.StartsWith('#'))
            {
                Span(sb, "c", line);
            }
            else if (line.IndexOf(':') is var colon and > 0)
            {
                Span(sb, "t", line[..colon]);
                Escape(sb, ":");
                var rest = line[(colon + 1)..];
                if (rest.Trim().Length > 0) Span(sb, "s", rest);
                else Escape(sb, rest);
            }
            else
            {
                Escape(sb, line);
            }
            if (li < lines.Length - 1) sb.Append('\n');
        }
        return sb.ToString();
    }

    public static string Plain(string text)
    {
        var sb = new StringBuilder(text.Length);
        Escape(sb, text);
        return sb.ToString();
    }

    // ------------------------------------------------------------- scanning

    private static int SkipString(string s, int i)
    {
        i++;
        while (i < s.Length)
        {
            if (s[i] == '\\') { i += 2; continue; }
            if (s[i] == '"') { i++; break; }
            i++;
        }
        return Math.Min(i, s.Length);
    }

    private static int SkipQuoted(string s, int i)
    {
        var quote = s[i];
        i++;
        while (i < s.Length)
        {
            if (s[i] == '\\') { i += 2; continue; }
            if (s[i] == quote) { i++; break; }
            i++;
        }
        return Math.Min(i, s.Length);
    }

    private static bool IsNumberStart(string s, int i) =>
        char.IsDigit(s[i]) || (s[i] == '-' && i + 1 < s.Length && char.IsDigit(s[i + 1]));

    private static int SkipNumber(string s, int i)
    {
        if (s[i] == '-') i++;
        while (i < s.Length && (char.IsDigit(s[i]) || s[i] is '.' or 'e' or 'E' or '+' or '-')) i++;
        return i;
    }

    private static bool TryLiteral(string s, ref int i, StringBuilder sb, string[] literals)
    {
        foreach (var lit in literals)
        {
            if (i + lit.Length > s.Length) continue;
            if (string.CompareOrdinal(s, i, lit, 0, lit.Length) != 0) continue;
            Span(sb, "k", lit);
            i += lit.Length;
            return true;
        }
        return false;
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
