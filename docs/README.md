Some of these docs were written with Claude Code in mind, e.g. they references `tasks` and `subagents`.

But for the most part they should work fairly well in other contexts (e.g. Cursor).

My workflow for starting a new epic is usually something like:

- `/model opus` - I usually use Opus where I want the most brains, e.g. upfront thinking & planning

- `We want to build X. Here's some background, desired features, concerns, etc. Be in @SOUNDING_BOARD_MODE.md`

- Discuss. This step takes the longest, answering the model's questions, considering various options & tradeoffs, etc.

-  If there's a new software library or specialist topic involved, I might say `"Follow instructions in @WRITE_DEEP_DIVE_AS_DOC.md for topic X`. That way, I'll have a new `docs/SOFTWARE_LIBRARY_X.md` that we can continually refer back to, containing up-to-date snippets and best practices from the web.

- `Create a new planning doc for this, following instructions in @WRITE_PLANNING_DOC.md`. Read that, check I'm happy with it, discuss/manually edit as needed. This is the key step. Because it has all the context from the deep dive and our conversation, the planning document is usually pretty rich.

- I occasionally `Run @CRITIQUE_OF_PLANNING_DOC.md` in Cursor with o3, and then feed that critique back to Claude to see if it wants to update its plan. (In practice, I mostly just rely on Claude, and only rope in o3 if we're doing something really tricky, or if we get struck.)

- `/compact` - this is a Claude Code command that clears the context window, adding a nice summary of what has been discussed before

- `/model sonnet` - I might switch over to Sonnet if I think the implementation part is straightforward. (With the more expensive [Anthropic Max Plan][https://www.anthropic.com/news/max-plan], I hit the rate limits for Opus sometimes).

- `Run @DO_PLANNING_DOC.md for [planning doc]`. Make a cup of tea. I have the Claude permissions mostly in YOLO mode, but it can't commit. The model will do a single stage (with lots of sub-actions), and then stop.

- Maybe manually test. Read the summary, perhaps also `Run @DEBRIEF_PROGRESS.md`. Often it'll be waiting for approval on a commit message.

- Run `/compact` and then `Do next stage of planning doc, as per @DO_PLANNING_DOC.md`

- Every so often:
  
  - Run `UPDATE_HOUSEKEEPING_DOCUMENTATION.md`.
  
  - Run `UPDATE_CLAUDE_INSTRUCTIONS.md`. It's critical that `CLAUDE.md` (or some equivalent Cursor rules) includes important stuff, e.g. a summary of `CODING_PRINCIPLES.md`, `CODING_GUIDELINES.md`, `DOCUMENTATION_ORGANISATION.md`). Then the prompts can be very short, and you can trust that the agent will find the right bit of the code reliably and without wasting too much context.
