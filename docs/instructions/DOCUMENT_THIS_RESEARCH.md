# DOCUMENT_RESEARCH.md - Research Documentation Instruction

Transform research findings into structured, actionable documentation that preserves knowledge and supports decision-making.

## When to Use This Instruction

Use this after completing research (via RESEARCH_TOPIC.md or other methods) when you need to:
- Create a permanent record of research findings
- Support decision-making with documented analysis
- Share research insights with others
- Build institutional knowledge
- Document the basis for product/technical decisions

## Documentation Types

Choose the appropriate format based on the research purpose:

### Decision Document
**Use when:** Research supports a specific decision (tool selection, approach choice, etc.)
**Structure:**
- **Decision Summary**: What was decided and why
- **Options Considered**: Alternatives evaluated with pros/cons
- **Research Basis**: Key findings that informed the decision
- **Implementation Notes**: Practical next steps
- **Future Considerations**: What to monitor or revisit

### Reference Guide
**Use when:** Research covers best practices, methodologies, or how-to information
**Structure:**
- **Overview**: Purpose and scope
- **Key Principles**: Core concepts and best practices
- **Implementation Guide**: Step-by-step guidance
- **Common Pitfalls**: What to avoid based on research
- **Resources**: Tools, libraries, further reading

### Landscape Analysis
**Use when:** Research maps out a domain, market, or technical area
**Structure:**
- **Executive Summary**: Key takeaways in 2-3 sentences
- **Current State**: What the landscape looks like now
- **Key Players**: Important tools, libraries, companies, people
- **Trends**: Where things are heading
- **Implications**: What this means for your context

### Investigation Report
**Use when:** Research was diagnostic (debugging, problem analysis)
**Structure:**
- **Problem Summary**: What was investigated and why
- **Findings**: What was discovered through research
- **Root Causes**: Underlying issues identified
- **Solutions**: Recommended approaches to address issues
- **Prevention**: How to avoid similar issues

## Documentation Standards

### Source Attribution
Always include:
- **Primary Sources**: Direct links to original research, documentation, official sources
- **Community Sources**: Links to discussions, forums, expert opinions with context
- **Tool Sources**: Version numbers, official documentation links
- **Research Methodology**: Brief note on how research was conducted

### Citation Format
Use consistent format throughout:
```
**Source Title** ([Author/Organization](URL)) - Brief description of relevance
```

Example:
```
**React Hook Form Documentation** ([React Hook Form](https://react-hook-form.com/)) - Official documentation covering performance benefits and API design
**"Comparing React Form Libraries 2025"** ([LogRocket Blog](https://blog.logrocket.com/...)) - Comprehensive comparison including bundle size and developer experience analysis
```

### Quality Indicators
For each major claim or recommendation, indicate:
- **Confidence Level**: High/Medium/Low based on source quality and consensus
- **Recency**: When information was published/last updated
- **Context**: Any limitations or specific conditions that apply

## Writing Guidelines

### Tone and Style
- **Objective**: Present findings without unnecessary opinion
- **Actionable**: Focus on what can be done with this information
- **Concise**: Respect reader's time while providing necessary detail
- **Structured**: Use clear headings and logical flow

### Content Organization
1. **Start with conclusion**: Put key insights and recommendations first
2. **Support with evidence**: Follow with research findings that support conclusions
3. **Provide context**: Include background needed to understand significance
4. **End with next steps**: Clear actions or considerations for moving forward

### Avoiding Common Pitfalls
- ❌ **Data dumping**: Don't just list all research findings without synthesis
- ❌ **Outdated information**: Clearly indicate when information might become stale
- ❌ **Missing context**: Don't assume readers have background knowledge
- ❌ **Weak attribution**: Always link back to original sources

## Document Metadata

Include at the top of each document:
```
---
Research Date: [Date research was conducted]
Documentation Date: [Date document was created]
Research Method: [Brief description - e.g., "Parallel web research using 4 specialized AI assistants"]
Review Date: [When this should be reviewed for currency - typically 6-12 months]
Status: [Current, Under Review, Outdated]
Related Documents: [Links to related research or decisions]
---
```

## Templates by Document Type

### Decision Document Template
```markdown
# [Decision Title]

## Decision Summary
[What was decided in 1-2 sentences]

## Context
[Why this decision was needed]

## Options Considered
### Option 1: [Name]
**Pros:** 
**Cons:**
**Sources:** 

### Option 2: [Name]
[Same structure]

## Decision Rationale
[Why the chosen option was selected based on research]

## Implementation Plan
[Next steps to execute the decision]

## Success Metrics
[How to know if this decision was right]

## Review Date
[When to reassess this decision]

## Sources
[Comprehensive source list with attribution]
```

### Reference Guide Template
```markdown
# [Topic] Reference Guide

## Overview
[Purpose and scope in 2-3 sentences]

## Key Principles
[Core concepts that emerged from research]

## Best Practices
### Practice 1: [Name]
**Description:** 
**Why it matters:** 
**Implementation:** 
**Sources:** 

## Common Pitfalls
[What to avoid based on research findings]

## Recommended Tools/Libraries
[Evidence-based recommendations with reasoning]

## Further Reading
[Curated list of high-quality sources for deeper exploration]

## Maintenance Notes
[What aspects of this guide might become outdated and when to review]
```

## Quality Checklist

Before finalizing documentation:

### Content Quality
- [ ] Key insights are clearly stated upfront
- [ ] Claims are supported by credible sources
- [ ] Contradictory information is acknowledged and addressed
- [ ] Practical implications are clearly explained
- [ ] Next steps or actions are specific and actionable

### Source Quality
- [ ] All major claims have source attribution
- [ ] Sources are recent enough for the topic (typically within 1-2 years)
- [ ] Mix of source types (official docs, expert analysis, community input)
- [ ] Source credibility has been evaluated
- [ ] URLs are working and properly formatted

### Document Structure
- [ ] Document follows appropriate template structure
- [ ] Headings create logical flow
- [ ] Content is scannable with bullet points and formatting
- [ ] Length is appropriate for purpose (typically 1-3 pages)
- [ ] Metadata is complete and accurate

### Future Utility
- [ ] Document will be useful to someone encountering this topic fresh
- [ ] Key context is included without assuming background knowledge
- [ ] Review/update timeline is realistic
- [ ] Related documents are cross-referenced

## File Naming and Location

### File Naming Convention
- **Decision docs**: `DECISION_[topic]_[YYYY-MM-DD].md`
- **Reference guides**: `REFERENCE_[topic].md`
- **Landscape analysis**: `LANDSCAPE_[domain]_[YYYY-MM-DD].md`
- **Investigation reports**: `INVESTIGATION_[problem]_[YYYY-MM-DD].md`

### Location Guidelines
- **Evergreen references**: `docs/reference/` (or equivalent)
- **Time-sensitive decisions**: `planning/` (or equivalent)
- **Technical guides**: `docs/reference/` with appropriate prefixes
- **Process documentation**: `docs/instructions/` (or equivalent)

## Maintenance and Updates

### Regular Review Process
- Set calendar reminders based on review dates in document metadata
- Monitor for changes in the researched domain that might affect conclusions
- Update source links if they become broken
- Archive outdated documents rather than deleting them

### Version Control
- Use Git commit messages to explain what changed and why
- Tag major updates with clear version indicators
- Link to previous versions when significant changes are made
- Document rationale for major revisions

This approach ensures research investments create lasting value through well-structured, maintainable documentation that supports ongoing decision-making and knowledge sharing. 