# Project Management Practices

This is a guide for writing planning/project management `.md` files, e.g. `planning/yyMMdda_complex_project.md`. These are for thinking through & documenting decisions, breaking down complex projects into multiple stages, and tracking progress.

Aim to keep these concise, and only include stuff explicitly agreed with the user.

If you're starting the doc from scratch, store it in `planning/`, and first ask the user questions about their project requirements to clarify key decisions. (Use MCP or run `date +"%y%m%d"` command first to get the current date for naming the file)

see also: `docs/WRITING_EVERGREEN_DOCS.md` for instructions on writing evergreen docs


## File naming conventions

Planning docs should follow this naming format: `yyMMdd[letter]_description_in_normal_case.md`

- Date prefix: `yyMMdd` format (e.g., `250526` for 26 May 2025)
- Auto-incrementing letter: append a letter (a, b, c...) based on creation order within the same day
  - First doc created on a given day gets `a`
  - Second doc gets `b`, and so on
  - This ensures files sort alphanumerically by creation date
  - Sometimes we might end up with multiple docs with the same day and letter (e.g. `250526a`, e.g if multiple agents were working simultaneously in separate Git worktrees) - don't worry if this happens
- Description: Use lowercase words separated by underscores
  - Exception: Keep proper capitalisation for acronyms like `ToC` (Table of Contents)
  - Example: `250526a_ToC_hierarchical_summary_tooltips.md`

Update this doc regularly to keep the actions up-to-date. When you change it, make minimal, focused changes, based on new user input.


## Document structure

Don't include a `Date` section at the top since it's implicit from the filename.


### Goal, context

- Clear problem/goal statement(s) at top, plus enough context/background to pick up where we left off
- If the goal is complex, break things down in detail about the desired behaviour.


### References

- Mention relevant evergreen docs (in `docs/`), other planning docs (in `planning/`), code files/functions, links, or anything else that could provide context, with a 1-sentence summary for each of what it's about/why it's relevant


### Principles, key decisions

- Include any specific principles/approaches or decisions that have been explicitly agreed with the user (over and above existing Cursor rules, project examples, best practices, etc).
- As you get new information from the user, update this doc so it's always up-to-date.


### Actions

- Break into lots of stages. Start with a really simple working v1, and gradually layer in complexity, ending each stage with passing tests and working code.
- List action in the order that they should be tackled
- Don't number the stages, so that it's easier to move them around without having to renumber everything
- Label the beginning of each action section with TODO, DONE, etc, updating task status as we go along
- Include subtasks with clear acceptance criteria
- Refer to specific docs, files/functions, examples, links, etc, so it's clear exactly what needs to be done
- Explicitly add tasks for writing automated tests, usually before writing code. (Perhaps one or two end-to-end tests first, then gradually adding more detailed tests as complexity grows). Explicitly add tasks for running the automated tests before ending each stage. see `docs/FRONTEND_TESTING.md`
- If there are actions that the user needs to do, add those in too, so we can track progress and remind the user.
- If this is a major piece of work, ask the user whether we should have an early action to create a `yyMMdd[letter]_complex_project` Git branch (and move over any changes). If so, then add a final action to merge that back into `main`.
- Add actions to update planning doc every so often with progress so far (perhaps at the end of every stage)
- Add actions to Git commit (perhaps at the end of every stage, perhaps use a subagent) - follow instructions in `docs/GIT_COMMITS.md`
- Add actions to stop & review with user where appropriate, e.g. when we get to a good stopping point, check changes to the user interface, etc
- Add actions to search the web where appropriate, e.g. when debugging, determining best practices, making use of 3rd-party libraries, etc
- Add actions to update relevant `docs/*.md` evergreen docs (see `docs/WRITING_EVERGREEN_DOCS`). If you think we need a new evergreen-doc, ask the user
- Explicitly say to use subagents for encapsulated tasks or where the task will create a lot of verbose content, e.g. checking for errors or browser console output with Playwright MCP, doing research

Example action:

```
- [ ] This is a top-level action description line
  - [ ] It can have sub-points that get ticked off
  - [x] This one has already been finished
```

# Appendix

Add any other important context here, e.g.
- Summary of web searching
- Example data
- Code snippets
- Other information that should be capture but doesn't fit neatly in the above sections, e.g. if there was a lengthy conversation, include a lot of richness/context/background/quotes to make sure it gets captured