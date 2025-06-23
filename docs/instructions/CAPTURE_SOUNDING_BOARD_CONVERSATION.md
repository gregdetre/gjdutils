# CAPTURE_SOUNDING_BOARD_CONVERSATION.md - Conversation Documentation Instruction

Transform rich sounding-board conversations into structured, preservable documents that capture nuance, decisions, and context for future reference and reflection.

## When to Use This Instruction

Use this to capture conversations that are:
- Long and rich with insights worth revisiting
- Exploratory discussions you want to mull over later
- Decision-making processes with valuable context
- Complex topics with multiple alternatives considered
- Conversations with research findings, sources, or citations worth preserving

## Core Principles

### Preserve vs Synthesize Balance
**Preserve verbatim (use quotes):**
- User background, intentions, and requirements
- Key decisions and rationale
- Specific terminology or framing the user prefers
- Important constraints or criteria
- Memorable insights or "aha" moments
- Specific proposals, examples, and code snippets discussed

**Synthesize and clean up:**
- Rambling or repetitive exchanges
- Scattered thoughts into organized themes
- AI responses (focus on key insights, not verbose explanations)
- Technical details that can be summarized
- Back-and-forth that reaches the same conclusion

### Source Preservation
Always capture:
- Links to external sources mentioned
- References to specific files, documentation, or code
- Citations from research or web searches
- Tool outputs or data that informed decisions
- Related conversations or documents

## Document Structure

Use flexible structure based on conversation flow, but generally follow this pattern:

### Standard Structure
```markdown
# [Conversation Topic] - [Date]

## Context & Goals
[Why this conversation happened, what prompted it]

## Key Background
[Important user context, constraints, requirements - use quotes for user's own words]

## Main Discussion
### [Theme/Topic 1]
[Synthesized discussion with key quotes and insights]

### [Theme/Topic 2]
[Continue for major themes that emerged]

## Alternatives Considered
[Options discussed with pros/cons - preserve user's language about preferences]

## Decisions Made
[Clear decisions with rationale - quote user's decision language]

## Open Questions
[What remains unresolved or needs further consideration]

## Next Steps
[Actions identified, if any]

## Sources & References
[All links, citations, related documents]

## Related Work
[Links to any documentation or implementation that resulted from this conversation]
```

### Alternative Structures

**For Exploratory Conversations:**
- Context & Motivation
- Key Insights & Discoveries  
- Areas for Further Exploration
- Questions Raised
- Sources & References

**For Problem-Solving Conversations:**
- Problem Definition
- Root Causes Discussed
- Solutions Explored
- Trade-offs Considered
- Recommended Approach
- Implementation Considerations

**For Research Review Conversations:**
- Research Question
- Key Findings Summary
- Alternative Interpretations
- Implications Discussed
- Gaps Identified
- Follow-up Research Needed

## Writing Guidelines

*Note: Take inspiration from documentation writing best practices for structure and clarity where applicable, but don't follow them rigidly - conversation docs have different goals and may need different approaches.*

### Capturing User Voice
Use direct quotes to preserve the user's:
- **Specific requirements**: "I want to make sure it cites better"
- **Preferences**: "I'd rather distill/restructure it, but without losing the nuance"
- **Constraints**: "It still sometimes seems to include last year in the query"
- **Decisions**: "Let's go with your recommendation"
- **Criteria**: "I just want to make sure it's as good as possible"

### Synthesis Techniques
When summarizing rambling or repetitive sections:
- **Extract core points**: What was the essential insight or concern?
- **Organize chronologically or thematically**: Group related points together
- **Preserve key terminology**: Use the user's preferred words for concepts
- **Note evolution of thinking**: "Initially considered X, but shifted to Y because..."
- **Include concrete details**: Preserve examples, code patterns, or technical approaches that illustrate key points

### Handling Technical Details
- **Summarize research findings**: Focus on implications, not full details
- **Link to sources**: Let readers dive deeper if needed  
- **Preserve methodology**: How research was conducted or decisions were made
- **Note tool outputs**: What data or results informed the conversation
- **Include specifics**: Preserve key examples, data points, or code snippets that informed decisions

## Source and Citation Handling

### External Sources
Format as:
```markdown
**[Source Title]** ([Organization/Author](URL)) - Brief relevance note
```

### Internal References
```markdown
- See `docs/reference/FILENAME.md` for related concepts
- Built on previous conversation: `docs/conversations/TOPIC_YYYY-MM-DD.md`
- Resulted in implementation: `docs/reference/NEW_FEATURE.md`
```

### Research Citations
When capturing research findings:
- Include the search queries used
- Note the research methodology (parallel AI assistants, etc.)
- Preserve key source URLs and assessment of credibility
- Distinguish between authoritative sources and anecdotal evidence
- Include specific examples, case studies, or data points that informed decisions

## Quality Guidelines

### Content Quality
- **Preserve nuance**: Don't oversimplify complex topics
- **Maintain context**: Include enough background for future readers
- **Balance detail with conciseness**: Rich but not overwhelming
- **Capture uncertainty**: Note where things are unclear or debated

### Structural Quality  
- **Clear headings**: Make it easy to scan and navigate
- **Logical flow**: Organize thoughts coherently
- **Complete sections**: Don't leave obvious gaps
- **Useful length**: Typically 2-5 pages depending on conversation depth

### Future Utility
- **Self-contained**: Can be understood without reading the original conversation
- **Actionable**: Clear what was decided or what next steps are
- **Connectable**: Links to related work and follow-up
- **Searchable**: Good keywords and clear topic identification

## File Naming and Organization

### Naming Convention
`yyMMdd[letter]_description_in_normal_case.md`

Use `date +"%y%m%d"` to get the current date for the prefix, then add description in lowercase words separated by underscores (except proper names/acronyms).

Example: `250616a_research_instructions_improvement.md`

### Location
Save to: `docs/conversations/` (or equivalent conversation documentation directory)

### Metadata
Include at top of document:
```markdown
---
Date: [Conversation date]
Duration: [Approximate length]
Type: [Decision-making, Exploratory, Problem-solving, Research Review]
Status: [Active, Resolved, Superseded]
Related Docs: [Links to resulting documentation]
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

## Integration with Other Documentation

### Link Forward
When this conversation leads to:
- **New documentation**: Link to resulting reference guides or decisions
- **Implementation work**: Reference related code changes or features
- **Further research**: Connect to follow-up research documentation
- **Process changes**: Link to updated procedures or guidelines

### Link Backward  
Reference:
- **Previous conversations**: Related discussions that informed this one
- **Existing documentation**: Relevant background material that was consulted
- **Research sources**: External material that provided context

## Maintenance

### Review Process
- Update "Related Docs" section when follow-up work is completed
- Add "Superseded by" notes if later conversations override decisions
- Archive conversations that are no longer relevant (but don't delete)

### Version Control
- Use meaningful commit messages when updating conversation docs
- Tag significant updates that change understanding or decisions
- Preserve conversation history even when circumstances change

This approach ensures valuable conversational insights are preserved in a structured, accessible format that serves multiple audiences and supports ongoing reflection and decision-making. 