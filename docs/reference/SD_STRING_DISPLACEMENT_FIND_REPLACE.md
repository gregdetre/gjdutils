# sd Find-Replace Tool ✓

sd is a modern, intuitive find-replace CLI tool designed for safe codebase refactoring, with excellent dry-run capabilities and literal string handling perfect for LLM automation.

**Important**: sd uses **regex mode by default**. Use `--string-mode` (or `-s`) for literal string matching to avoid issues with special characters in file paths.

## See Also

- Official documentation: [sd GitHub](https://github.com/chmln/sd)
- Installation: Available via Rust cargo, Homebrew (macOS), or package managers

## Key Benefits

- **Safety-first**: True dry-run preview mode with `--preview`
- **LLM-friendly**: Literal string mode eliminates regex escaping issues
- **Modern design**: Clean, intuitive syntax focused on find-replace only
- **Simple syntax**: Readable command structure with clear options
- **Path-friendly**: Handles file paths with special characters seamlessly

## Installation

```bash
# Rust (cross-platform)
cargo install sd

# macOS (Homebrew)
brew install sd

# Ubuntu/Debian
sudo apt install sd
```

## Usage Patterns

### Dry-Run Mode (Recommended for LLMs)

```bash
# Preview changes without modifying files
sd --preview "old-string" "new-string" file.txt

# Preview with literal strings (no regex)
sd --preview --string-mode "app/[slug]/page.tsx" "app/[id]/page.tsx" **/*.tsx

# Short form
sd -ps "old-string" "new-string" .
```

### Apply Changes Mode

```bash
# Apply changes after preview looks good
sd --string-mode "old-string" "new-string" file.txt

# Recursive across directories
sd -s "old/path" "new/path" **/*.md
```

## Common Use Cases

### Path Updates (File Paths with Special Characters)
```bash
# Preview import path changes (dry-run)
sd --preview --string-mode "from '@/old/path'" "from '@/new/path'" **/*.{ts,tsx}

# Apply after preview
sd -s "from '@/old/path'" "from '@/new/path'" **/*.{ts,tsx}

# Update file references in documentation
sd -ps "/old/location/" "/new/location/" **/*.md
```

### String Replacements
```bash
# Preview function name changes
sd --preview "oldFunctionName" "newFunctionName" **/*.{ts,tsx,js,jsx}

# Update configuration values (literal strings)
sd -ps "OLD_CONFIG_VALUE" "NEW_CONFIG_VALUE" .
```

### Documentation Updates
```bash
# Preview cross-reference updates
sd --preview --string-mode "old-doc-name.md" "new-doc-name.md" **/*.md
```

## Safety Best Practices

1. **Always preview first**: Use `--preview` (or `-p`) to see exactly what will change
2. **Use literal strings**: Use `--string-mode` (or `-s`) for file paths and exact matches
3. **Test scope first**: Start with single files, then expand to directories
4. **Use version control**: Commit before running large refactors
5. **Verify with build**: Run build and tests after changes

## Advanced Options

```bash
# Case-insensitive matching
sd --ignore-case "CamelCase" "snake_case" .

# Preview multiline replacements with literal strings
sd --preview --string-mode --multiline "old\nline" "new\nline" file.txt

# Include hidden files and directories
sd --hidden ".oldValue" ".newValue" .

# Use shell globbing for file selection
sd -ps "oldKey" "newKey" **/*.json
```

## Troubleshooting

**No matches found**: Check file paths and use preview mode
```bash
# Debug: preview what would be matched
sd --preview "search-term" "replacement" **/*.md
```

**Special character issues**: Use literal string mode for paths
```bash
# Problematic (regex metacharacters like [, ], ., *, etc.)
sd "app/[slug]/page.tsx" "app/[id]/page.tsx" .

# Safe (literal strings)
sd --string-mode "app/[slug]/page.tsx" "app/[id]/page.tsx" .
```

**Permission errors**: Ensure files are writable and not locked by editors

## Integration with Development Workflow

sd integrates seamlessly with codebase development:

- **File moves**: Update all references after moving files (use `--string-mode`)
- **Refactoring**: Rename functions, variables, and imports across the codebase
- **Documentation**: Update cross-references when files are renamed (literal strings)
- **Configuration**: Update environment variables and configuration keys
- **LLM automation**: Perfect for programmatic find-replace with predictable behavior

## Key Options Summary

- `--preview` (`-p`): Show changes without applying them (dry-run)
- `--string-mode` (`-s`): Treat search/replace as literal strings (no regex)
- `--ignore-case` (`-i`): Case-insensitive matching
- `--multiline` (`-m`): Enable multiline matching
- `--hidden`: Include hidden files and directories

## Perfect for LLM Usage

- **Predictable**: Literal string mode eliminates regex escaping surprises
- **Safe**: Dry-run mode shows exactly what will change
- **Simple**: Clean syntax that's easy to generate programmatically
- **Path-friendly**: Handles file paths with brackets, dots, and other special characters