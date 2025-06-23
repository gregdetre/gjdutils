# Writing evergreen documentation

see also: 
- `WRITE_PLANNING_DOC.md` - for writing ephemeral decision/planning docs
- `UPDATE_HOUSEKEEPING_DOCUMENTATION.md` - for keeping documentation current every so often


# What are evergreen docs?

This is for writing evergreen, general documentation on how the system works.

These should be a concise, clear, well-structured, complete-enough, up-to-date description of things. By "complete-enough", they should cover most of the important topics, if only to signpost to where more information can be found, or to the code itself.

They should refer to one another, and avoid too much overlap in content, so that if information changes, we ideally only need to change the documentation in one place.


# Format

They should be written in Markdown, stored as `../reference/TOPIC_NAME.md` for reference documentation or `TOPIC_NAME.md` for instructional content.

## Filename Guidelines

Choose descriptive filenames that clearly indicate the document's content:

- **Be specific**: `UPLOAD_DOCUMENT_PROCESSING_PIPELINE.md` instead of just `UPLOAD.md`
- **Include context**: `NAVIGATION_COMPONENT_DESIGN.md` instead of just `NAVIGATION.md`
- **Keep existing names**: Where possible, include the current name as a prefix (e.g., `SETUP_DEVELOPMENT_ENVIRONMENT.md` keeps `SETUP`)
- **Group related docs**: Use similar prefixes so related docs sort together (e.g., all `DATABASE_*.md` files)
- **Maintain prefix conventions**: Keep category prefixes (DATABASE_, TESTING_, API_, etc.)

Good examples:
- `DATABASE_INTEGRATION_REFERENCE.md`
- `TESTING_AUTOMATION_OVERVIEW.md`
- `API_CLIENT_INTEGRATION.md`
- `AUTHENTICATION_SECURITY.md`


## Document structure

They might be organised into something like the following sections. Use your judgment. Probably only a few of these will be relevant for each doc, feel free to rename them, etc.


### Introduction

2-sentence summary of the topic, and what the document covers.

### See also

Bullet-point list of other relevant docs, code, urls, or other resources that provide related information, or more detail. Provide a 1-sentence summary or explanation of how each one is relevant. 

Examples of good cross-references:
- `WRITE_PLANNING_DOC.md` - for information about writing ephemeral decision/planning docs
- `src/components/example.tsx` - implementation of features described here
- `planning/YYYYMMDD_feature_planning.md` - historical decision context
- External URLs when relevant (e.g., library documentation)

Add references to and from this new doc (e.g. in relevant code, planning docs in `planning/*.md`, etc) - use a subagent for this

#### Cross-Reference Best Practices

- **Update documentation organisation index** if your project has one
- **Link to canonical source** (e.g. functions, files, docs, urls, etc) for detailed information rather than duplicating
- **Provide 1-sentence context** with each link explaining its relevance
- **Use relative paths** for internal documentation links
- **Avoid content duplication** - if information exists elsewhere, link to it

Add references to and from this new doc (e.g. in relevant code, planning docs, etc) - use parallel AI assistance for this


### Principles, key decisions

- Include any specific principles/approaches or decisions that have been explicitly agreed with the user (over and above existing coding rules, project examples, best practices, etc).
- As you get new information from the user, update this doc so it's always up-to-date.

### [Provide a few detailed sections here, depending on the topic]

Include as appropriate:
- high-level overview, architecture
- common patterns, howtos
- examples
- gotchas
- limitations
- troubleshooting
- planned future work


### Documenting Systems in Transition

When documenting systems that are changing (e.g., architectural migrations):

1. **Clearly distinguish states**:
   - **Current State**: How the system works today
   - **Target State**: The intended future architecture
   - **Migration Status**: Progress and timeline if known

2. **Reference decisions**: Link to planning docs or architecture decision records for rationale

3. **Update incrementally**: As migration progresses, update the documentation

Example:
```markdown
## Database Architecture

**Current State**: Uses legacy schema approach
**Target State**: New optimized schema with performance improvements
**Migration Status**: Schema designed, code updates pending

see `../reference/ARCHITECTURE_DECISIONS.md` for migration rationale
```


### Appendix

Add any other important context here, e.g.
- example data
- other information that should be captured but doesn't fit neatly in the above sections


# Maintenance

## Review Frequency

Regular documentation review ensures accuracy:
- **After major features** - Update immediately after implementation
- **During housekeeping** - Monthly review recommended
- **When outdated** - Fix immediately when noticed
- **Before milestones** - Ensure docs reflect current state

see `UPDATE_HOUSEKEEPING_DOCUMENTATION.md` for the complete housekeeping process

## Common Pitfalls to Avoid

1. **Information duplication** - Creates maintenance burden when things change
2. **Vague status descriptions** - Be specific about implementation state
3. **Missing cross-references** - Always link to related documentation
4. **Outdated examples** - Ensure code samples match current patterns
5. **Forgotten transitions** - Update docs as systems migrate

## Quality Checklist

Before committing documentation:
- [ ] Cross-references are valid and helpful
- [ ] No contradictions with other documents
- [ ] Examples match current code patterns
- [ ] Transitional states are clearly marked
- [ ] "See also" sections are comprehensive