namespace PowerPlatformApis.Browser.Rendering;

/// <summary>How the code surface is dressed: editor tabs, or a console prompt.</summary>
public enum CodeChrome
{
    /// <summary>Tabs and a language label, for files and payloads.</summary>
    Editor,

    /// <summary>A single title beside the prompt, for commands.</summary>
    Console
}

public enum CodeLanguage
{
    PlainText,
    Json,
    Bash,
    Http,
    CSharp,
    Xml,
    Yaml
}

public static class CodeLanguageInfo
{
    /// <summary>The label shown in the chrome, matching keel's language names.</summary>
    public static string Label(this CodeLanguage language) => language switch
    {
        CodeLanguage.Json => "JSON",
        CodeLanguage.Bash => "Bash",
        CodeLanguage.Http => "HTTP",
        CodeLanguage.CSharp => "C#",
        CodeLanguage.Xml => "XML",
        CodeLanguage.Yaml => "YAML",
        _ => "Text"
    };

    /// <summary>keel's language dot colours.</summary>
    public static string? Dot(this CodeLanguage language) => language switch
    {
        CodeLanguage.Json => "#bcae3b",
        CodeLanguage.Bash => "#4eaa25",
        CodeLanguage.Http => "var(--accent)",
        CodeLanguage.CSharp => "#9b6dff",
        CodeLanguage.Xml => "#e37933",
        CodeLanguage.Yaml => "#cb4b16",
        _ => null
    };
}
