# AI Model Critiques - API Approach

Automated approach for critiquing planning documents using direct API calls with comprehensive codebase context generation.

## See also

- `docs/instructions/GATHER_DIVERSE_INPUTS_AND_CRITIQUES_ON_PLANNING_DOCS_FROM_OTHER_AI_MODELS.md` - **Start here**: Core intent and workflow overview
- Generic critique script (adapt to your project's structure)
- `docs/instructions/CRITIQUE_OF_PLANNING_DOC.md` - Critique methodology used by AI models

## Overview

This document details the **API approach** for obtaining AI model critiques of planning documents. For context on why this critique process exists and the core workflow, see `docs/instructions/GATHER_DIVERSE_INPUTS_AND_CRITIQUES_ON_PLANNING_DOCS_FROM_OTHER_AI_MODELS.md`.

This approach addresses reliability issues with agentic workflows by using a single, comprehensive API call to AI models. The script gathers relevant codebase context and sends everything for analysis.

**Key advantages over agentic approaches:**
- **Reliability**: Single API call vs complex agentic workflow
- **Control**: Precise control over what context is included
- **Speed**: No back-and-forth file reading delays
- **Cost efficiency**: One large prompt vs many small interactions
- **Reproducibility**: Same context produces consistent results

## Prerequisites

### Required Environment Variables
- `OPENAI_API_KEY` in `.env.local` - Your OpenAI API key (for o3 access)
- `ANTHROPIC_API_KEY` in `.env.local` - Your Anthropic API key (for Claude access)
- Other provider keys as needed

### Required Dependencies
A code context generation tool is recommended:
```bash
# Example with code2prompt (Rust version)
brew install code2prompt

# Alternative installation methods:
# Via install script: curl -fsSL https://raw.githubusercontent.com/mufeedvh/code2prompt/main/install.sh | sh
# Via Cargo: cargo install code2prompt

# Verify installation
code2prompt --version
```

### System Requirements
- Node.js with TypeScript support (tsx)
- curl (for API calls)
- Git repository context
- Context generation tool (code2prompt or similar)

## Basic Usage

### Simple Critique
```bash
# Adapt script name and path to your project
./scripts/ai-critique-as-api.ts planning/my-feature-plan.md
```

### With Options
```bash
# Include test files in context
./scripts/ai-critique-as-api.ts --include-tests planning/my-plan.md

# Use different models (multi-provider support)
./scripts/ai-critique-as-api.ts --model openai:o3:latest planning/my-plan.md
./scripts/ai-critique-as-api.ts --model anthropic:claude-opus-4 planning/my-plan.md
./scripts/ai-critique-as-api.ts --model google:gemini-2.5-pro planning/my-plan.md

# Verbose output with token counts
./scripts/ai-critique-as-api.ts --verbose planning/my-plan.md
```

## How It Works

### 1. **Context Generation Phase**
The script uses a context generation tool with optimized settings:

**Included file types:**
- `*.ts, *.tsx, *.js, *.jsx` - Application code
- `*.md` - Documentation and planning files
- `*.json, *.yml, *.yaml` - Configuration files
- `*.sql` - Database schemas and migrations

**Automatically excluded:**
- **Uses .gitignore**: Respects project's .gitignore for consistent exclusions
- `*.test.*, *.spec.*, __tests__/*` - Test files (unless `--include-tests`)

**Key features enabled:**
- **Line numbers**: For precise code references in critique
- **Token counting**: Cost transparency and context management
- **Directory tree**: Project structure understanding
- **.gitignore support**: Automatic exclusion of generated/temporary files

### 2. **Unified LLM Integration**
The script integrates with your project's LLM system:

1. **Template system**: Type-safe prompt generation
2. **Multi-provider support**: OpenAI, Anthropic, Google via model strings
3. **Consistent interface**: Unified API across all providers
4. **Usage tracking**: Automatic token counting and cost calculation

### 3. **Model Configuration**
- **Model strings**: `provider:model:version` format (e.g., `openai:o3-pro:latest`)
- **Automatic provider selection**: Based on model string
- **API key validation**: Handled by provider factory
- **Configurable settings**: Temperature, max tokens, etc.

## Output Files

All outputs are saved to `planning/critiques/` with timestamps:

### Context File
**Format**: `CONTEXT_FOR__[doc-name]__YYMMDD_HHMM.md`
**Contains**: Complete codebase context with file structure, implementation code, and documentation

### API Response
**Format**: `[model]__CRITIQUE_OF__[doc-name]__YYMMDD_HHMM.json`
**Contains**: Raw API response including critique content and usage statistics

## File Selection Strategy

### Automated Relevance Detection
The script uses a **comprehensive inclusion** approach rather than trying to guess relevance:

**Core principle**: Include all implementation and documentation files, exclude noise
- No manual file curation required
- Consistent context across different planning documents
- Reduces risk of missing important context

### When to Include Tests (`--include-tests`)
**Include test files when:**
- Planning document involves testing strategy changes
- Critique needs to understand current test patterns
- Implementation changes affect existing test architecture

**Exclude test files when (default):**
- Focus is on architecture and design decisions
- Token optimization is important
- Planning is high-level strategic discussion

## Token Management

### Cost Optimization
- **Context size**: Typically 20k-50k tokens for medium codebases
- **Response limit**: Default 4000 tokens (configurable with `--max-tokens`)
- **Model selection**: Choose based on reasoning capability needs

### Token Monitoring
```bash
# Check context size before sending
./scripts/ai-critique-as-api.ts --verbose planning/my-plan.md
```

The script displays token counts and estimated costs when using `--verbose` flag.

## Error Handling and Recovery

### Common Issues and Solutions

**"Context generation tool not found"**
```bash
# Install appropriate tool (example with code2prompt):
brew install code2prompt

# Verify installation:
code2prompt --version
```

**"API key missing for model [model]"**
```bash
# Add appropriate API key to .env.local:
echo "OPENAI_API_KEY=your-openai-key" >> .env.local
echo "ANTHROPIC_API_KEY=your-anthropic-key" >> .env.local  
echo "GOOGLE_GENERATIVE_AI_API_KEY=your-google-key" >> .env.local
```

**"Model not available"**
```bash
# Check available models in your project's model configuration
# Or use a known model like:
./scripts/ai-critique-as-api.ts --model anthropic:claude-sonnet-4 planning/doc.md
```

**"Planning document not found"**
```bash
# Verify file path:
ls -la planning/your-document.md
```

### Recovery Guidance
The script should provide specific recovery instructions for each error type, including:
- Command-line examples for debugging
- File permission checks
- Network connectivity tests
- Documentation references

## Advanced Configuration

### Custom Model Selection
```bash
# Use different model variants
./scripts/ai-critique-as-api.ts --model o3-2024-12-17 planning/my-plan.md
```

### Response Length Control
```bash
# Longer responses for complex documents
./scripts/ai-critique-as-api.ts --max-tokens 6000 planning/complex-plan.md
```

### File Type Customization
For specialized critique needs, modify the file filter parameters in the script.

## Integration with Existing Workflow

### Relationship to Current Process
This approach can serve as:
- **Primary method**: Replace agentic CLI workflow for reliability
- **Backup approach**: Fallback when CLI approach has issues
- **Complementary tool**: Use both approaches for different critique aspects

### Workflow Integration
This approach implements the core workflow described in the overview document:

1. **Write planning document** following `docs/instructions/WRITE_PLANNING_DOC.md`
2. **Commit planning doc** (creates pre-critique baseline)
3. **Run automated critique**: `./scripts/ai-critique-as-api.ts planning/doc.md`
4. **Process critique response** using methodology from overview
5. **Update planning document** based on feedback
6. **Commit revised version** with critique summary

See the overview document for details on processing critique responses and incorporating feedback.

## Quality and Limitations

### Strengths
- **Comprehensive context**: Includes all relevant code and documentation
- **Consistent results**: Same input produces similar critique quality
- **Fast execution**: Single API call vs multiple interactions
- **Cost predictable**: Fixed token usage patterns
- **Error resilient**: Clear failure modes and recovery

### Current Limitations
- **Static file selection**: No dynamic relevance scoring
- **Large token usage**: Includes more context than strictly necessary
- **No iterative refinement**: Single-shot analysis vs conversational critique
- **Model dependency**: Requires API access and model availability

### Future Enhancements
- **Intelligent file filtering**: Use embeddings for relevance scoring
- **Template customization**: Different prompt templates for different critique focuses
- **Multi-model support**: Enhanced support for different AI providers
- **Iterative critique**: Support follow-up questions and refinement

This approach provides a reliable foundation for AI-assisted planning document critique, enabling systematic external validation for critical planning decisions.