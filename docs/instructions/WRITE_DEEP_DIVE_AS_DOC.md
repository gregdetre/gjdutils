# Write Deep Dive as Documentation

Do a deep dive on the web about the topic that the user has asked about. If you need more clarification about the requirements to focus the search fruitfully, ask questions (ideally upfront). If you need more context from files, investigate for relevant code & docs.

Before you start, run `date` to get today's date, in case you need to assess how recent the search results are.

Then write this up as a detailed reference doc, following the instructions in `WRITE_EVERGREEN_DOC.md`. Include URL links/references (as well as mentions of your own code/docs etc), so you can track down the original sources later if you need to.

## Process Guidelines

### 1. Clarify the Scope
Before diving into research, ask:
- What specific aspects of the topic are most important?
- What's the intended use case or application?
- Are there particular problems you're trying to solve?
- How deep should the technical detail go?
- What's the target audience for this documentation?

### 2. Research Strategy
- **Start broad** - Get an overview of the topic and ecosystem
- **Go specific** - Focus on the aspects most relevant to your needs
- **Check recency** - Note dates on articles, especially for fast-moving technologies
- **Multiple sources** - Cross-reference information from different authorities
- **Practical focus** - Prioritize actionable information over theory

### 3. Documentation Structure
Follow `WRITE_EVERGREEN_DOC.md` format:
- **Overview** - What is this technology/concept?
- **Use cases** - When and why to use it
- **Getting started** - Quick setup or hello world
- **Key concepts** - Essential understanding
- **Best practices** - Proven approaches and patterns
- **Common gotchas** - Known issues and how to avoid them
- **Resources** - Links to official docs, tutorials, tools

### 4. Source Attribution
- **Direct links** - Include URLs for all referenced sources
- **Date notation** - Note when sources were published/accessed
- **Authority assessment** - Prefer official docs, established experts, recent sources
- **Code attribution** - Reference any code examples with their source

## Content Quality Standards

### Technical Accuracy
- Cross-reference information across multiple sources
- Test code examples if possible
- Note when information is based on specific versions
- Flag areas where practices are evolving quickly

### Practical Value
- Include working code examples with explanations
- Document common setup issues and solutions
- Provide migration paths from alternative solutions
- Include performance and security considerations

### Maintainability
- Structure content for easy updates
- Use clear section headers for findability
- Include "last updated" dates for time-sensitive content
- Note areas that may need frequent revision

## Research Areas to Cover

### Technology Overview
- What problem does it solve?
- How does it compare to alternatives?
- What's the ecosystem and community like?
- What are the licensing and cost considerations?

### Implementation Details
- Installation and setup requirements
- Configuration options and best practices
- Integration patterns with common frameworks
- Testing and debugging approaches

### Real-World Usage
- Performance characteristics
- Scalability considerations
- Security implications
- Common deployment patterns

### Troubleshooting
- Known issues and workarounds
- Common error messages and solutions
- Debugging tools and techniques
- Community resources for help

Remember: The goal is to create a reference that will save time and prevent common mistakes in future projects. Focus on the information that would be most valuable to someone implementing this technology.