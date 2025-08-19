# Research Potential Library Changes & Gotchas

## Objective

Identify areas of your codebase where someone new might get tripped up, and determine what information can be gathered, and what preparation/documentation and other improvements can be made to help them avoid these issues.

## Research Methodology

### Phase 1: Background Research
- Read foundational documentation:
    - Project documentation organisation guide
    - Architecture and site organisation docs
    - `instructions/WRITE_DEEP_DIVE_AS_DOC.md`
    - `instructions/UPDATE_CLAUDE_INSTRUCTIONS.md`
    - Other relevant code and documentation

- Run `date` to get today's date/time for timeline context.

### Phase 2: Library Research
For each library in your dependency manifest (`package.json`, `requirements.txt`, `Cargo.toml`, etc.) and architecture documentation, research:
- **Known gotchas and common pitfalls**
- **API changes in the last 12 months** (breaking changes, deprecations, new patterns)
- **Version compatibility issues**
- **Security advisories or updates**
- **Performance considerations or changes**
- **Community-reported issues and solutions**

### Phase 3: Codebase Analysis
Review the codebase for:
- **Complex/unconventional patterns** that might need extra documentation
- **Unclear code sections** where intent, rationale, or usage is ambiguous
- **Cross-component interactions** with surprising or non-obvious behaviour
- **Areas lacking sufficient comments** where context would prevent mistakes
- **Potential maintenance hazards** or brittle implementations

### Phase 4: Ask User to Clarify Requirements
Ask the user questions if you need to, based on what you've found so far, to suggest further actions, and to shape the recommendations that you provide.

Following the user's response, do any final research needed, so that recommendations can be very concrete.

### Phase 5: Prioritised Recommendations
Wait until you've received responses to your questions before starting to generate recommendations in a planning doc.

Generate actionable recommendations balancing:
- **Priority/risk assessment** of identified issues. Don't be hyperbolic, e.g. don't label something 'Critical' unless it truly is. Don't sweat the small stuff.
- **Likelihood that there will be a problem in this area, and that this documentation would help**
- **Documentation burden** vs. benefit (avoiding over-documentation)

Example recommendations (though these are just examples - use your judgment about what's valuable/relevant for the project you're working on):
- Write a deep dive doc on a particular library, emphasising how the API for it has changed in the new version
- Update the deployment script or instructions to avoid a particular gotcha
- Update the instructions for running migrations to ban potentially destructive actions (e.g. dropping all tables)
- Create a doc for adding features of a particular type, that references relevant docs/code, provides examples/snippets/patterns

## Execution Strategy

### Task Management and Parallel AI Assistance
Follow instructions in `instructions/TASKS_SUBAGENTS.md` if available. It'll be necessary to make heavy but careful use of parallel AI assistance in order to avoid filling up the context window.

When delegating to parallel AI assistance, provide:
- **Clear scope and objectives** for their specific research area
- **Current date context** for timeline-sensitive research
- **References to relevant documentation** they should consult
- **Specific libraries or code areas** to focus on
- **Format expectations** for their findings
- **Decision-making authority** and escalation criteria

Tell parallel AI assistants to output detailed enough evidence/logging that you can retrace their steps (e.g. which URLs or parts of the code their output is based on). Coordinate the findings from parallel AI assistants into coherent recommendations.

### Focus Areas by Technology Stack

#### Frontend/JavaScript Projects
- **React/Vue/Angular**: Lifecycle changes, hooks patterns, state management
- **Build tools**: Webpack, Vite, bundler configuration gotchas
- **CSS frameworks**: Breaking changes, deprecated classes, new patterns
- **TypeScript**: Strict mode changes, new language features impact

#### Backend Projects
- **Framework changes**: Breaking API changes, middleware patterns
- **Database libraries**: Migration tools, query builder changes
- **Authentication**: Security patches, token handling changes
- **API clients**: Rate limiting, retry logic, SDK updates

#### DevOps/Infrastructure
- **Container configs**: Base image updates, security patches
- **CI/CD pipelines**: Action/tool version compatibility
- **Cloud services**: API changes, pricing model shifts
- **Monitoring tools**: Configuration format changes

## Output Format

Deliver findings as a planning document following the format in `instructions/WRITE_PLANNING_DOC.md`:

1. **Planning document structure**:
   - Goal and context section explaining the research scope
   - Critical findings with risk assessment (urgent/high/medium priority)
   - Stages & actions with checkboxes for implementation tracking
   - Implementation roadmap for addressing identified issues
   - Appendix with research evidence and sources

2. **File naming**: Use format appropriate for your project structure (e.g., `planning/yyMMdda_research_library_changes_gotchas.md`)

3. **Content organisation**:
   - Executive summary of key risks and recommendations
   - Library-specific findings with actionable items
   - Codebase improvement opportunities prioritised by impact
   - Reference URLs and evidence for all findings

## Research Questions by Category

### Dependency Health
- Are we using outdated versions with known vulnerabilities?
- Are there breaking changes in recent versions we should prepare for?
- Do our dependencies have security advisories or critical patches?
- Are there performance improvements available in newer versions?

### Code Quality & Maintainability
- Where are the most complex or hard-to-understand parts of the codebase?
- What patterns or practices might confuse new team members?
- Are there undocumented assumptions or implicit dependencies?
- What would break if key contributors weren't available?

### Development Experience
- What causes the most friction for new developers getting started?
- Are there common mistakes that could be prevented with better tooling?
- What parts of the build/test/deploy process are brittle?
- Where could better documentation or automation save time?

IMPORTANT: Do not make any implementation changes yet, until authorised by the user. The planning document should only contain research findings and recommended actions.