# Tasks and Subagents

Use subagents where appropriate:
- They are especially valuable as a way to avoid filling up your context window, e.g. for running a battery of tests, Playwright/curl/browser automation, MCPs with verbose output
- They are also a good fit for encapsulated & well-defined tasks, i.e. tasks that don't need the full context of the conversation so far, and/or where we only need a summary of what was done in order to proceed
- Use subagents in parallel where possible (because this is faster), but only if there isn't a dependency between tasks (e.g. the output of this one is useful as input for the next)
- Give them lots of background/careful instructions so that they can make good decisions, e.g. about goals, point them to relevant docs/code, what we've been changing, gotchas & things to avoid, relevant environment variables like $PORT for browser automation, using your test framework, the current date/time from `date`, and anything else that will help them to be effective but correct/careful.
- Tell subagents what to be cautious of, and to abort and provide feedback on what happened if there are problems or surprises (to avoid them going rogue and doing more harm than good)

Use the task/todo list when you have more than a couple of things to track, or where ordering matters, when there are subagents involved, or if you think it will help.
