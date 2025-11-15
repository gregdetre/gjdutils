Transform conversations into structured, preservable documents that capture nuance, decisions, and context for future reference and reflection.

## Core Principles

### Preserve vs Synthesize Balance

**Capture/preserve**: (always quote verbatim for user input)
- Background/context, intentions, requirements, decisions, principles, preferences, rationale, terminology, framings, constraints, criteria, etc from the user, etc
- Memorable insights, tradeoffs, recommendations, etc
- Specific proposals, examples, and code snippets discussed
- Citations/references, e.g. to specific files, documentation, conversations, or code, external sources mentioned, web research
- Tool outputs or data that informed decisions

**Synthesize and clean up:**
- Rambling or repetitive exchanges
- Scattered thoughts into organized themes
- AI responses (focus on key insights, not verbose explanations)
- Technical details that can be summarized
- Back-and-forth that reaches the same conclusion
- Dead-ends

This approach ensures valuable conversational insights are preserved in a structured, accessible format that serves multiple audiences and supports ongoing reflection and decision-making. 


## File Naming and Organization

`yyMMdd[letter]_description_in_normal_case.md`

Use `npx tsx scripts/sequential-datetime-prefix.ts docs/conversations/` if available, otherwise use `date +"%y%m%d"` to get the current date for the prefix, then add description in lowercase words separated by underscores (except proper names/acronyms).

Example: `250616a_research_instructions_improvement.md`

Save to: `docs/conversations/` (or equivalent conversation documentation directory)


### Metadata

Include frontmatter metadata at top of document, e.g.:

```markdown
---
Date: [Conversation date, e.g. 2025-June-16 & timestamp]
Type: [Decision-making, Exploratory, Problem-solving, Research Review]
---
```


## Common Conversation Patterns

### Decision-Making Conversations
Focus on:
- What options were considered and why
- What criteria drove the decision
- What concerns or trade-offs were discussed
- The final decision and rationale
- Specific proposals and examples that influenced the decision

### Exploratory Conversations
Focus on:
- What questions or curiosities drove the discussion
- What insights or patterns emerged
- What new questions arose
- What areas warrant further investigation

### Problem-Solving Conversations
Focus on:
- How the problem was defined and understood
- What root causes were identified
- What solutions were brainstormed
- What approach was recommended and why

### Research Review Conversations
Focus on:
- What research question prompted the investigation
- What key findings emerged
- How findings were interpreted or applied
- What gaps or follow-up research were identified
- Specific examples, data points, or methodological insights that stood out

## References

Provide comprehensive signposting/citations/references where applicable. Link forwards and backwards.

