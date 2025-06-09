# Project Management Practices

This is a guide for writing planning/project management `.md` files, e.g. `planning/yyMMdda_complex_project.md`. These are for thinking through & documenting decisions, breaking down complex projects into multiple stages, and tracking progress.

Aim to keep these concise, but emphasise & clearly capture all the decisions, responses, and requirements from the user.

If you're starting the doc from scratch:
- (Use MCP or run `date +"%y%m%d"` command first to get the current date for naming the file)
- Store it in `planning/`, and first ask the user questions about their project requirements to clarify key decisions.
- See `SOUNDING_BOARD_MODE.md`

see also: `WRITE_EVERGREEN_DOC.md` for instructions on writing evergreen docs


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

- Include any specific principles/approaches or decisions that have been explicitly agreed with the user (over and above existing project rules, examples, best practices, etc).
- As you get new information from the user, update this doc so it's always up-to-date.
- If there are any surprises/issues, stop immediately, and discuss with the user before proceeding.


### Stages & actions

Overall approach:
- Break into lots of stages. Start with a really simple working v1, and gradually layer in complexity, ending each stage with passing tests and working code.
- List stages and actions in the order that they should be tackled
- Don't number the stages, so that it's easier to move them around without having to renumber everything
- Use `[ ]` and `[x]` checkboxes to indicate todo/done.
- Include subtasks with clear acceptance criteria
- Refer to specific docs, files/functions, examples, links, etc, so it's clear exactly what needs to be done
- Explicitly add tasks for writing automated tests, usually before writing code. (Perhaps one or two end-to-end tests first, then gradually adding more detailed tests as complexity grows). Explicitly add tasks for running the automated tests before ending each stage.
- If there are actions that the user needs to do, add those in too, so we can track progress and remind the user.
- If this is a major piece of work, ask the user whether we should have an early action to create a `yyMMdd[letter]_complex_project` Git branch (and move over any changes). If so, then add a final action to merge that back into `main`.
- Add actions to stop & review with user where appropriate, e.g. when we get to a good stopping point, to manually check changes to the user interface, etc
- Add actions to search the web where appropriate, e.g. when debugging, determining best practices, making use of 3rd-party libraries, etc
- Add actions to update relevant `docs/*.md` evergreen docs (see `WRITE_EVERGREEN_DOC.md`). 
- If you think we need a new evergreen-doc, ask the user
- Explicitly say to use subagents for encapsulated tasks or where the task will create a lot of verbose content, e.g. checking for errors or browser console output with Playwright MCP, doing research
- Try to surface potential risks early. For example, if the whole plan rests on the library being able to do X, let's do a quick trial to make sure that works).
- Try to organise the stages so that we frontload the business value, so that we could stop partway. For example, get it working for the primary/most valuable use-case first.

As the very, very first preparatory action (if applicable to your project):
- Run sync scripts or pull latest changes to make sure we've pulled the latest changes from `main` before we start (to make merge conflicts less likely).

At the end of every stage:
- Follow instructions in `DEBRIEF_PROGRESS.md` (if available) to output a summary of where things stand, and update the planning doc with progress so far.
- Git commit (following instructions in `GIT_COMMITS.md`, including use a subagent).

As a very final action:
- Move the doc to `planning/finished/` and commit.

Example stages & action (no need to include the words `TODO` or `DONE` explicitly, since the `[ ]` todo-checkboxes capture that):

```
### Stage: High-level description of this stage
- [ ] This is a top-level action
  - [ ] It can have sub-actions that get ticked off
    - You can add bulletpoint notes with extra detail/context to help plan & shape future actions

### ✅ This stage has already been completed
  - ✅ This action has already been completed
    - 📔 You could journal about useful/unexpected discoveries when you update progress on completed tasks
  - ❌ This action has failed/been skipped
```

# Appendix

Add any other important context here, e.g.
- Summary of web searching
- Example data
- Code snippets & mentions
- Relevant tests
- Rich background, quotes, and context, especially from conversations/decisions from the user
- Alternative approaches that were considered but discarded - describe the desiderata, tradeoffs, and especially the approach we did picked and the rationale.
- Other information that should be captured but didn't fit neatly in the above sections
