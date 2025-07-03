# Getting Diverse AI Model Critiques on Planning Documents - Overview

Process for obtaining external critiques of planning documents using different AI models to improve decision quality and catch blind spots.

## See also

- `docs/instructions/WRITE_PLANNING_DOC.md` - Guidelines for writing planning documents (includes this critique stage)
- `docs/instructions/CRITIQUE_OF_PLANNING_DOC.md` - Methodology for systematic planning document critique

## Intent and Purpose

External AI model critiques provide valuable perspective on planning documents by:
- **Identifying assumptions and blind spots** that human reviewers might miss
- **Suggesting alternative approaches** from different architectural perspectives  
- **Highlighting potential risks and edge cases** before implementation begins
- **Validating technical decisions** against industry best practices
- **Providing independent assessment** free from project-specific biases

This process is **mandatory** for all planning documents to ensure quality and catch issues early in the development cycle.

## Core Workflow

### 1. Prepare Planning Document
- Write initial planning document following `docs/instructions/WRITE_PLANNING_DOC.md`
- **Commit the planning doc first** (creates pre-critique baseline for comparison)

### 2. Specify Feedback Focus
Before running critique, specify what type of feedback is most valuable:
- **Technical architecture** - Focus on implementation approach and technical decisions
- **Risk identification** - Emphasize potential problems, edge cases, and failure modes  
- **Process optimization** - Review project stages, sequencing, and workflow efficiency
- **Best practices** - Validate against industry standards and proven patterns
- **Scope and prioritization** - Assess feature selection and MVP boundaries

### 3. Run External Critique
Choose one of the available approaches:

**API Approach (Recommended)**:
```bash
# Basic usage - adapt script name and path to your project
./scripts/ai-critique-as-api.ts planning/your-planning-doc.md

# With options
./scripts/ai-critique-as-api.ts --include-tests planning/my-plan.md
./scripts/ai-critique-as-api.ts --model openai:o3:latest planning/my-plan.md
./scripts/ai-critique-as-api.ts --verbose planning/my-plan.md
```
- Single comprehensive API call with full codebase context
- Highly reliable execution vs agentic workflows
- Multi-provider support (OpenAI, Anthropic, Google)
- Comprehensive context generation with optimized file selection

**CLI Approach (Experimental)**:
```bash
# Generic script name - adapt to your project's script location  
./scripts/ai-critique-cli.sh planning/your-planning-doc.md
```
- Agentic conversation-based critique
- More interactive but less reliable
- See: `docs/instructions/GATHER_DIVERSE_INPUTS_AND_CRITIQUES_ON_PLANNING_DOCS_FROM_OTHER_AI_MODELS_CODEX_CLI_APPROACH.md`

### 4. Process Critique Response
- **Switch AI assistant to enhanced reasoning mode** for processing critique
- AI assistant should:
  - Read and analyze the critique thoroughly
  - Search web for additional context if needed
  - Exercise independent judgment on which suggestions are valuable
  - Propose specific changes/responses to user for discussion
  - Avoid accepting suggestions uncritically

### 5. Incorporate Feedback
- User and AI assistant discuss critique insights
- Update planning document based on agreed changes
- Add critique documentation section (see template below)
- **Commit revised planning document**

## Planning Document Template Addition

Add this section to planning documents after critique:

```markdown
## External Critique

**Critique Date**: [Date]
**Model**: [Model used, e.g. OpenAI o3-pro, Claude Opus]  
**Approach**: [API/CLI]
**Raw Output**: `planning/critiques/[model]__CRITIQUE_OF__[doc-name]__[timestamp].[json|jsonl]`
**Feedback Focus**: [What type of feedback was requested]
**Key Insights**: [Summary of useful feedback points]
**Changes Made**: [What was incorporated and rationale]
**Rejected Suggestions**: [What was not incorporated and why]
```

## Approach Comparison

### API Approach
**Strengths:**
- Highly reliable single API call
- Comprehensive codebase context
- Predictable cost and timing
- Clear error handling

**When to use:**
- Standard planning document critique
- Need reliable, consistent results
- Want comprehensive context inclusion

### CLI Approach  
**Strengths:**
- Interactive, conversational critique
- Can ask follow-up questions
- More natural dialogue flow
- Dynamic context (agent chooses what files to examine)
- Conversational refinement capability

**Current limitations:**
- ⚠️ **Experimental/Reliability Issues**: Not working reliably due to:
  - Timeout issues during long conversations
  - Broken function calls in agentic workflows
  - Inconsistent execution across different planning documents
- Complex error recovery
- Higher computational cost than single API calls

**How it works (when working):**
1. **Initial document read**: AI agent reads the planning document
2. **Context gathering**: Agent explores relevant codebase files
3. **Interactive analysis**: Agent asks questions and builds understanding
4. **Comprehensive critique**: Agent provides detailed feedback
5. **Follow-up clarification**: Agent can respond to questions about the critique

**When to consider:**
- Experimental scenarios (when reliability improves)
- Need interactive refinement
- API approach insufficient for specific use cases

## API Approach - Detailed Implementation

### Prerequisites

**Required Environment Variables:**
- `OPENAI_API_KEY` in `.env.local` - Your OpenAI API key (for o3 access)
- `ANTHROPIC_API_KEY` in `.env.local` - Your Anthropic API key (for Claude access)
- `GOOGLE_GENERATIVE_AI_API_KEY` in `.env.local` - Your Google API key (for Gemini access)

**Required Dependencies:**
```bash
# Example with code2prompt (Rust version)
brew install code2prompt

# Alternative installation methods:
# Via install script: curl -fsSL https://raw.githubusercontent.com/mufeedvh/code2prompt/main/install.sh | sh
# Via Cargo: cargo install code2prompt

# Verify installation
code2prompt --version
```

**System Requirements:**
- Node.js with TypeScript support (tsx)
- curl (for API calls)
- Git repository context
- Context generation tool (code2prompt or similar)

### How It Works

**1. Context Generation Phase**
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

**2. Unified LLM Integration**
The script integrates with your project's LLM system:

1. **Template system**: Type-safe prompt generation
2. **Multi-provider support**: OpenAI, Anthropic, Google via model strings
3. **Consistent interface**: Unified API across all providers
4. **Usage tracking**: Automatic token counting and cost calculation

**3. Model Configuration**
- **Model strings**: `provider:model:version` format (e.g., `openai:o3-pro:latest`)
- **Automatic provider selection**: Based on model string
- **API key validation**: Handled by provider factory
- **Configurable settings**: Temperature, max tokens, etc.

### Output Files

All outputs are saved to `planning/critiques/` with timestamps:

**Context File:**
- **Format**: `CONTEXT_FOR__[doc-name]__YYMMDD_HHMM.md`
- **Contains**: Complete codebase context with file structure, implementation code, and documentation

**API Response:**
- **Format**: `[model]__CRITIQUE_OF__[doc-name]__YYMMDD_HHMM.json`
- **Contains**: Raw API response including critique content and usage statistics

### File Selection Strategy

**Automated Relevance Detection:**
The script uses a **comprehensive inclusion** approach rather than trying to guess relevance:

**Core principle**: Include all implementation and documentation files, exclude noise
- No manual file curation required
- Consistent context across different planning documents
- Reduces risk of missing important context

**When to Include Tests (`--include-tests`):**
- Planning document involves testing strategy changes
- Critique needs to understand current test patterns
- Implementation changes affect existing test architecture

**Exclude test files when (default):**
- Focus is on architecture and design decisions
- Token optimization is important
- Planning is high-level strategic discussion

### Token Management

**Cost Optimization:**
- **Context size**: Typically 20k-50k tokens for medium codebases
- **Response limit**: Default 4000 tokens (configurable with `--max-tokens`)
- **Model selection**: Choose based on reasoning capability needs

**Token Monitoring:**
```bash
# Check context size before sending
./scripts/ai-critique-as-api.ts --verbose planning/my-plan.md
```

The script displays token counts and estimated costs when using `--verbose` flag.

### Error Handling and Recovery

**Common Issues and Solutions:**

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

### Advanced Configuration

**Custom Model Selection:**
```bash
# Use different model variants
./scripts/ai-critique-as-api.ts --model o3-2024-12-17 planning/my-plan.md
```

**Response Length Control:**
```bash
# Longer responses for complex documents
./scripts/ai-critique-as-api.ts --max-tokens 6000 planning/complex-plan.md
```

**File Type Customization:**
For specialized critique needs, modify the file filter parameters in the script.

## Quality Criteria for Major Planning Documents

While critique is mandatory for all docs, the following characteristics indicate particularly important docs requiring extra attention:
- **Core architecture changes** - Affects fundamental system structure
- **High implementation cost/risk** - Significant time investment or technical complexity
- **Novel approaches** - Using unfamiliar techniques or experimental patterns
- **User-facing changes** - Impacts user experience or interface design
- **Cross-cutting concerns** - Affects multiple system components

## Configuration Requirements

Both approaches require:
- Appropriate API keys in `.env.local` (OpenAI, Anthropic, Google, etc.)
- Access to project context via project documentation
- Following critique methodology in `docs/instructions/CRITIQUE_OF_PLANNING_DOC.md`
- Context generation tool (code2prompt or similar) for API approach
- Node.js with TypeScript support (tsx) for script execution

This process complements human review and provides systematic external validation for critical planning decisions, ensuring higher quality outcomes through diverse AI perspectives.