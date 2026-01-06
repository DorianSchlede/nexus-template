# cc-tools (Go) Findings

**Repository**: cc-tools (Go implementation of Claude Code utilities)
**Author**: Josh Symonds (@Veraticus)
**License**: MIT
**Analysis Date**: 2025-12-31

## Executive Summary

cc-tools is a high-performance Go implementation providing statusline generation and MCP management for Claude Code. It demonstrates excellent patterns for dependency injection, interface-based design, terminal handling, and configuration management. The codebase is well-structured with comprehensive test coverage and clean separation of concerns.

---

## Key Patterns

### 1. Dependency Injection via Interfaces

The codebase uses interface-based dependency injection consistently, enabling excellent testability:

```go
// Dependencies contains all external dependencies.
type Dependencies struct {
    FileReader    FileReader
    CommandRunner CommandRunner
    EnvReader     EnvReader
    TerminalWidth TerminalWidth
    CacheDir      string
    CacheDuration time.Duration
}

// Interface definitions
type FileReader interface {
    ReadFile(path string) ([]byte, error)
    Exists(path string) bool
    ModTime(path string) (time.Time, error)
}

type CommandRunner interface {
    Run(command string, args ...string) ([]byte, error)
}

type EnvReader interface {
    Get(key string) string
}

type TerminalWidth interface {
    GetWidth() int
}
```

**Key Insight**: Every external dependency (filesystem, commands, environment, terminal) is abstracted behind an interface, allowing for easy mocking in tests and flexibility in production.

### 2. Adapter Pattern for Default Implementations

Default implementations wrap OS operations with proper error handling:

```go
// DefaultFileReader implements FileReader using the OS.
type DefaultFileReader struct{}

func (f *DefaultFileReader) ReadFile(path string) ([]byte, error) {
    content, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading file %s: %w", path, err)
    }
    return content, nil
}

// DefaultCommandRunner implements CommandRunner using exec.
type DefaultCommandRunner struct{}

func (c *DefaultCommandRunner) Run(command string, args ...string) ([]byte, error) {
    const commandTimeout = 5 * time.Second
    ctx, cancel := context.WithTimeout(context.Background(), commandTimeout)
    defer cancel()
    cmd := exec.CommandContext(ctx, command, args...)
    output, err := cmd.Output()
    if err != nil {
        return nil, fmt.Errorf("running command %s: %w", command, err)
    }
    return output, nil
}
```

**Key Insight**: All commands have a timeout (5 seconds default) to prevent hangs. Error messages include context about what operation failed.

### 3. Graceful Degradation Pattern

The statusline tool falls back gracefully when errors occur:

```go
func main() {
    out := output.NewTerminal(os.Stdout, os.Stderr)

    input, err := io.ReadAll(os.Stdin)
    if err != nil {
        // Fallback prompt output to stdout
        out.Raw(" > ")
        os.Exit(0)
    }

    result, err := runStatuslineWithInput(reader)
    if err != nil {
        // Fallback prompt output to stdout
        out.Raw(" > ")
        os.Exit(0)
    }
    out.Raw(result)
}
```

**Key Insight**: Never crash - always provide a usable fallback (simple prompt in this case).

---

## Hook Output Handling

### Exit Code Protocol

Claude Code hooks use specific exit codes for communication:

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| 0 | Success | stdout shown in transcript mode (Ctrl-R) |
| 2 | Blocking error | stderr fed back to Claude to process |
| Other | Non-blocking error | stderr shown to user, execution continues |

### HookFormatter Implementation

Raw ANSI codes for hook output compatibility:

```go
type HookFormatter struct{}

const (
    ansiRed    = "\033[0;31m"
    ansiGreen  = "\033[0;32m"
    ansiYellow = "\033[0;33m"
    ansiReset  = "\033[0m"
)

func (h *HookFormatter) FormatSuccess(message string) string {
    return fmt.Sprintf("%s%s%s", ansiGreen, message, ansiReset)
}

func (h *HookFormatter) FormatWarning(message string) string {
    return fmt.Sprintf("%s%s%s", ansiYellow, message, ansiReset)
}

func (h *HookFormatter) FormatError(message string) string {
    return fmt.Sprintf("%s%s%s", ansiRed, message, ansiReset)
}

func (h *HookFormatter) FormatBlockingError(format string, args ...any) string {
    message := fmt.Sprintf(format, args...)
    return h.FormatError(message)
}
```

**Key Insight**: Uses raw ANSI codes rather than a styling library for hook output to ensure compatibility with Claude Code's expectations.

### Hook Input JSON Schema

Hooks receive JSON via stdin with structured data:

```go
type Input struct {
    Model struct {
        ID          string `json:"id"`
        Provider    string `json:"provider"`
        DisplayName string `json:"display_name"`
    } `json:"model"`
    Cost struct {
        TotalCostUSD     float64 `json:"total_cost_usd"`
        InputTokens      int     `json:"input_tokens"`
        OutputTokens     int     `json:"output_tokens"`
        CacheReadTokens  int     `json:"cache_read_input_tokens"`
        CacheWriteTokens int     `json:"cache_creation_input_tokens"`
    } `json:"cost"`
    GitInfo struct {
        Branch       string `json:"branch"`
        IsGitRepo    bool   `json:"is_git_repo"`
        HasUntracked bool   `json:"has_untracked"`
        HasModified  bool   `json:"has_modified"`
    } `json:"git_info"`
    Workspace struct {
        ProjectDir string `json:"project_dir"`
        CurrentDir string `json:"current_dir"`
        CWD        string `json:"cwd"`
    } `json:"workspace"`
    TranscriptPath string `json:"transcript_path"`
}
```

---

## Status Line Implementation

### Architecture Overview

The statusline is built with a three-section layout:
1. **Left Section**: Directory path + Model name/icon
2. **Middle Section**: Context bar (progress indicator for token usage)
3. **Right Section**: Git branch, hostname, K8s context, AWS profile, devspace

### Component-Based Rendering

```go
type Component struct {
    Color string
    Text  string
}

func (s *Statusline) buildRightSection(data *CachedData, availableWidth int) string {
    components := s.collectRightComponents(data, awsProfile, maxLengths)
    return s.renderComponents(components)
}
```

### Dynamic Width Calculation

Sophisticated terminal width detection with multiple fallback methods:

```go
func (t *DefaultTerminalWidth) GetWidth() int {
    widthMethods := []func() int{
        t.getTestOverride,      // CLAUDE_STATUSLINE_WIDTH env var
        t.getColumnsEnv,        // COLUMNS env var
        t.getTmuxIfAvailable,   // tmux display-message
        t.getFromStderr,        // term.GetSize on stderr
        t.getFromStdout,        // term.GetSize on stdout
        t.getFromStdin,         // term.GetSize on stdin
        t.getFromTTY,           // /dev/tty
        t.getSSHWidth,          // SSH_TTY env var
        getTputWidth,           // tput cols command
        getSttyWidth,           // stty size command
    }

    for _, method := range widthMethods {
        if width := method(); width > 0 {
            return width
        }
    }
    return t.getDefault() // 200 chars
}
```

**Key Insight**: Multiple fallback strategies ensure terminal width detection works in various environments (tmux, SSH, containers, etc.).

### Catppuccin Color Scheme

Uses 24-bit true color ANSI codes with the Catppuccin Mocha theme:

```go
type CatppuccinMocha struct{}

func (c CatppuccinMocha) LavenderBG() string { return "\033[48;2;180;190;254m" } // #b4befe
func (c CatppuccinMocha) GreenBG() string { return "\033[48;2;166;227;161m" }     // #a6e3a1
func (c CatppuccinMocha) SkyBG() string { return "\033[48;2;137;220;235m" }       // #89dceb
// ... etc

func (c CatppuccinMocha) NC() string { return "\033[0m" } // Reset
```

### Powerline Icons

Unicode powerline symbols for visual appeal:

```go
const (
    LeftChevron  = ""
    LeftCurve    = ""
    RightCurve   = ""
    RightChevron = ""

    GitIcon      = " "
    AwsIcon      = " "
    K8sIcon      = "☸ "
    HostnameIcon = " "
    ContextIcon  = " "

    // Progress bar characters
    ProgressLeftEmpty  = ""
    ProgressLeftFull   = ""
    ProgressMidEmpty   = ""
    ProgressMidFull    = ""
    ProgressRightEmpty = ""
    ProgressRightFull  = ""
)
```

### Context Bar with Progress Indicator

Visual context usage indicator with color-coded thresholds:

```go
func (s *Statusline) getContextColors(percentage float64) (string, string, string) {
    const (
        greenThreshold  = 40.0
        yellowThreshold = 60.0
        peachThreshold  = 80.0
    )
    switch {
    case percentage < greenThreshold:
        return s.colors.GreenBG(), s.colors.GreenFG(), s.colors.GreenLightBG()
    case percentage < yellowThreshold:
        return s.colors.YellowBG(), s.colors.YellowFG(), s.colors.YellowLightBG()
    case percentage < peachThreshold:
        return s.colors.PeachBG(), s.colors.PeachFG(), s.colors.PeachLightBG()
    default:
        return s.colors.RedBG(), s.colors.RedFG(), s.colors.RedLightBG()
    }
}
```

### Token Metrics from Transcript

Parses JSONL transcript files to calculate context length:

```go
func (s *Statusline) getTokenMetrics(transcriptPath string) TokenMetrics {
    // Parse JSONL transcript file
    lines := strings.Split(string(content), "\n")

    for _, line := range lines {
        var msg struct {
            Message struct {
                Usage struct {
                    InputTokens              int `json:"input_tokens"`
                    OutputTokens             int `json:"output_tokens"`
                    CacheReadInputTokens     int `json:"cache_read_input_tokens"`
                    CacheCreationInputTokens int `json:"cache_creation_input_tokens"`
                } `json:"usage"`
            } `json:"message"`
            IsSidechain       bool   `json:"isSidechain"`
            IsApiErrorMessage bool   `json:"isApiErrorMessage"`
            Timestamp         string `json:"timestamp"`
        }

        // Track most recent main chain entry for context length calculation
        if !msg.IsSidechain && !msg.IsApiErrorMessage {
            // Calculate context length
        }
    }

    return metrics
}
```

---

## Configuration Patterns

### XDG-Compliant Config Paths

```go
func getConfigFilePath() string {
    // Check XDG_CONFIG_HOME first
    if xdgConfig := os.Getenv("XDG_CONFIG_HOME"); xdgConfig != "" {
        return filepath.Join(xdgConfig, "cc-tools", "config.json")
    }

    // Default to ~/.config/cc-tools/config.json
    homeDir, err := os.UserHomeDir()
    if err != nil {
        return "config.json" // Fallback
    }

    return filepath.Join(homeDir, ".config", "cc-tools", "config.json")
}
```

### Configuration Manager Pattern

```go
type Manager struct {
    configPath string
    config     *ConfigValues
}

type ConfigValues struct {
    Statusline StatuslineConfigValues `json:"statusline"`
}

type StatuslineConfigValues struct {
    Workspace    string `json:"workspace"`
    CacheDir     string `json:"cache_dir"`
    CacheSeconds int    `json:"cache_seconds"`
}
```

### Configuration Commands

```bash
cc-tools config list              # Show all settings with defaults
cc-tools config show              # View raw JSON
cc-tools config get KEY           # Get specific value
cc-tools config set KEY VALUE     # Set value
cc-tools config reset KEY         # Reset to default
cc-tools config reset             # Reset all to defaults
```

### YAML Configuration (example-config.yaml)

```yaml
notifications:
  ntfy_topic: my-claude-notifications
```

### JSON Configuration (runtime)

```json
{
  "statusline": {
    "workspace": "",
    "cache_dir": "/dev/shm",
    "cache_seconds": 20
  }
}
```

---

## Debug Logging Implementation

### Thread-Safe Logger

```go
type Logger struct {
    mu       sync.Mutex
    file     *os.File
    filePath string
    enabled  bool
}

func (l *Logger) Log(format string, args ...any) {
    if !l.enabled || l.file == nil {
        return
    }

    l.mu.Lock()
    defer l.mu.Unlock()

    timestamp := time.Now().Format("2006-01-02 15:04:05.000")
    message := fmt.Sprintf(format, args...)
    _, _ = fmt.Fprintf(l.file, "[%s] %s\n", timestamp, message)
}
```

### Debug Commands

```bash
cc-tools debug enable    # Enable for current directory
cc-tools debug disable   # Disable for current directory
cc-tools debug status    # Check if enabled
cc-tools debug filename  # Show log file path
cc-tools debug list      # List all directories with debug enabled
```

### Invocation Logging

All cc-tools invocations are logged when debug is enabled:

```go
func debugLog() {
    timestamp := time.Now().Format("2006-01-02 15:04:05.000")
    fmt.Fprintf(f, "[%s] cc-tools invoked\n", timestamp)
    fmt.Fprintf(f, "Args: %v\n", os.Args)
    fmt.Fprintf(f, "Environment:\n")
    fmt.Fprintf(f, "  CLAUDE_HOOKS_DEBUG: %s\n", os.Getenv("CLAUDE_HOOKS_DEBUG"))
    fmt.Fprintf(f, "  Working Dir: %s\n", workingDir)
    if len(stdinDebugData) > 0 {
        fmt.Fprintf(f, "Stdin: %s\n", string(stdinDebugData))
    }
}
```

---

## Unique Go-Specific Approaches

### 1. String Builder for Efficient Concatenation

```go
func (s *Statusline) buildLeftSection(...) string {
    var sb strings.Builder

    sb.WriteString(s.colors.LavenderFG())
    sb.WriteString(LeftCurve)
    sb.WriteString(s.colors.LavenderBG())
    // ... more writes

    return sb.String()
}
```

### 2. Runewidth for Unicode Handling

Uses `github.com/mattn/go-runewidth` for proper Unicode width calculation:

```go
func truncateText(text string, maxWidth int) string {
    width := runewidth.StringWidth(text)
    if width <= maxWidth {
        return text
    }
    const ellipsisWidth = 1
    return runewidth.Truncate(text, maxWidth-ellipsisWidth, "") + "..."
}
```

### 3. Context-Aware Command Execution

```go
func (c *DefaultCommandRunner) Run(command string, args ...string) ([]byte, error) {
    const commandTimeout = 5 * time.Second
    ctx, cancel := context.WithTimeout(context.Background(), commandTimeout)
    defer cancel()
    cmd := exec.CommandContext(ctx, command, args...)
    output, err := cmd.Output()
    // ...
}
```

### 4. ANSI Stripping for Width Calculation

```go
func stripAnsi(text string) string {
    var result strings.Builder
    inEscape := false
    for _, r := range text {
        switch {
        case r == '\033':
            inEscape = true
        case inEscape:
            if r == 'm' {
                inEscape = false
            }
        default:
            result.WriteRune(r)
        }
    }
    return result.String()
}
```

### 5. Lipgloss for Styled Output

```go
type Terminal struct {
    stdout io.Writer
    stderr io.Writer
    styles map[Level]lipgloss.Style
}

func defaultStyles() map[Level]lipgloss.Style {
    return map[Level]lipgloss.Style{
        Info:    lipgloss.NewStyle().Foreground(lipgloss.Color("#89dceb")),
        Success: lipgloss.NewStyle().Foreground(lipgloss.Color("#a6e3a1")),
        Warning: lipgloss.NewStyle().Foreground(lipgloss.Color("#f9e2af")),
        Error:   lipgloss.NewStyle().Foreground(lipgloss.Color("#f38ba8")),
        Debug:   lipgloss.NewStyle().Foreground(lipgloss.Color("#94e2d5")),
    }
}
```

---

## Notes for Implementation

### 1. Interface-First Design
- Define interfaces before implementations
- Keep interfaces small and focused (FileReader, CommandRunner, EnvReader)
- Use dependency injection for all external operations

### 2. Graceful Degradation
- Never crash the user's terminal
- Always provide fallback output
- Silent failure for non-critical operations (debug logging)

### 3. Performance Considerations
- Use `/dev/shm` for cache files (RAM-based filesystem)
- Command timeouts (5 seconds for single commands, 2 seconds for terminal width detection)
- 20-second cache duration for expensive operations
- Use `strings.Builder` for string concatenation

### 4. Terminal Compatibility
- Multiple fallback methods for terminal width detection
- Support for tmux, SSH, containers
- Test override environment variables for deterministic testing

### 5. Color and Styling
- Use 24-bit true color ANSI codes for modern terminals
- Catppuccin color scheme for consistency
- Powerline symbols for visual appeal
- Always reset colors after styled output

### 6. Configuration
- XDG-compliant config paths
- JSON format with structured types
- Support for both config files and environment variables
- Clear separation of defaults and user overrides

### 7. Testing Support
- Environment variable overrides for testing (`CLAUDE_STATUSLINE_WIDTH`, `CLAUDE_STATUSLINE_HOSTNAME`, etc.)
- Interface-based design enables easy mocking
- Debug environment variables (`DEBUG_WIDTH`, `DEBUG_CONTEXT`)

### 8. Hook Protocol
- Exit code 0 = success, stdout for transcript
- Exit code 2 = blocking error, stderr for Claude
- JSON input via stdin
- JSON or plain text output via stdout

---

## File Structure Reference

```
cc-tools/
├── cmd/
│   ├── cc-tools/              # Main CLI
│   │   ├── main.go            # Entry point
│   │   ├── config.go          # Config subcommand
│   │   ├── debug.go           # Debug subcommand
│   │   └── mcp.go             # MCP subcommand
│   └── cc-tools-statusline/   # Standalone statusline binary
│       └── main.go
├── internal/
│   ├── config/
│   │   ├── config.go          # Config loading
│   │   └── manager.go         # Config management
│   ├── debug/
│   │   ├── config.go          # Debug config
│   │   └── logger.go          # Debug logger
│   ├── mcp/
│   │   └── mcp.go             # MCP server management
│   ├── output/
│   │   ├── hook.go            # Hook-specific formatting
│   │   ├── output.go          # Terminal output
│   │   └── table.go           # Table formatting
│   ├── shared/
│   │   ├── colors.go          # Color definitions
│   │   ├── debug_paths.go     # Debug file paths
│   │   ├── dependencies.go    # Shared deps
│   │   └── project.go         # Project detection
│   └── statusline/
│       ├── adapters.go        # Default implementations
│       ├── colors.go          # Catppuccin colors
│       ├── helpers.go         # Utility functions
│       ├── icons.go           # Unicode icons
│       ├── render.go          # Rendering logic
│       ├── statusline.go      # Main statusline
│       └── terminal.go        # Terminal width
├── reference/
│   ├── hooks.md               # Hook documentation
│   └── statusline.md          # Statusline docs
├── example-config.yaml        # YAML config example
├── example-config.toml        # TOML config example
├── CLAUDE.md                  # Development guide
└── README.md                  # User documentation
```

---

## Summary

cc-tools demonstrates excellent Go patterns for building CLI tools that integrate with Claude Code:

1. **Clean Architecture**: Separation between interfaces, implementations, and commands
2. **Testability**: Interface-based design with dependency injection
3. **Robustness**: Graceful degradation, timeouts, and fallbacks
4. **Performance**: Caching, efficient string handling, RAM-based file operations
5. **User Experience**: Beautiful terminal output with proper Unicode handling
6. **Developer Experience**: Debug logging, configuration management, clear documentation

These patterns can be directly applied to the Nexus Advanced Hook System implementation.
