# Context Window, Tasks, and Subagents

Use tasks whenever there's more than a couple of things to keep track of.

Use subagents where appropriate:
- e.g. for running a battery of tests, curl, Playwright/Puppeteer MCP or other browser automation, other verbose output, Git commits, any other verbose-output, and anywhere else where you think it's a good fit
- They are especially valuable as a way to avoid filling up your context window
- They are also a good fit for encapsulated & well-defined tasks, i.e. tasks that don't need the full context of the conversation so far, and/or where we only need a summary of what was done in order to proceed
- Use subagents in parallel where possible (because this is faster), but only if there isn't a dependency between tasks (e.g. the output of this one is useful as input for the next)
- Give them lots of background so that they can make good decisions, e.g. about goals, point them to relevant docs/code, what we've been changing, gotchas & things to avoid, relevant environment variables like $PORT for browser automation, using your test framework, the current date/time from `date`, and anything else that will help them to be effective but correct/careful.
- Tell subagents what to be cautious of, and to abort and provide feedback on what happened if there are problems or surprises (to avoid them going rogue and doing more harm than good)

## When to Use Tasks

Use the task/todo system when you have:
- More than 2-3 things to track
- Multi-step processes that span multiple conversations
- Complex workflows that benefit from status tracking
- Parallel workstreams that need coordination

## When to Use Subagents

Subagents are ideal for:
- **Verbose operations**: Testing, builds, git operations, browser automation
- **Encapsulated tasks**: Well-defined work that doesn't need full conversation context
- **Parallel work**: Independent tasks that can be done simultaneously
- **Context preservation**: Keeping the main conversation focused on high-level decisions

## Best Practices

### For Task Management
- Break complex work into specific, actionable items
- Update status in real-time as work progresses
- Mark tasks complete immediately when finished
- Only have one task "in_progress" at a time

### For Subagent Delegation
- Provide rich context about goals and constraints
- Point to relevant documentation and code
- Specify what to be cautious about
- Include environment details (ports, test frameworks, etc.)
- Ask for summaries rather than full details
- Set clear success/failure criteria

### Integration
- Use tasks to track what subagents are working on
- Have subagents report back with summaries
- Use task status to coordinate multiple subagents
- Keep the main conversation focused on planning and decisions