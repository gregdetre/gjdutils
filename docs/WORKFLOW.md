Some of these docs were written with Claude Code in mind, e.g. they reference `tasks` and `subagents`.

But for the most part they should work fairly well in other contexts (e.g. Cursor).

My workflow for starting a new epic is usually something like:

- **Switch to best model** - I usually use Claude Opus 4 where I want the most brains, e.g. upfront thinking & planning (though I'm not certain it's really that much smarter than Sonnet)
  - Claude Code: `/model opus` 
  - Cursor: Switch your model to Claude Sonnet 4 in the model selector

- `We want to build X. Here's some background, desired features, concerns, etc. Be in @instructions/SOUNDING_BOARD_MODE.md`

- Discuss. This step takes the longest, answering the model's questions, considering various options & tradeoffs, etc.

-  If there's a new software library or specialist topic involved, I might say `"Follow instructions in @instructions/WRITE_DEEP_DIVE_AS_DOC.md for topic X`. That way, I'll have a new `docs/SOFTWARE_LIBRARY_X.md` that we can continually refer back to, containing up-to-date snippets and best practices from the web.

- `Create a new planning doc for this, following instructions in @instructions/WRITE_PLANNING_DOC.md`. Read that, check I'm happy with it, discuss/manually edit as needed. This is the key step. Because it has all the context from the deep dive and our conversation, the planning document is usually pretty rich.

- I occasionally `Run @instructions/CRITIQUE_OF_PLANNING_DOC.md` in Cursor with o3, and then feed that critique back to Claude to see if it wants to update its plan. (In practice, I mostly just rely on Claude, and only rope in o3 if we're doing something really tricky, or if we get struck.)

- **Clear context** - Clear the context window, adding a nice summary of what has been discussed before
  - Claude Code: `/compact`
  - Cursor: Start a new chat (there's no equivalent to `/compact` in Cursor, but fortunately you can just reference the planning doc)

- **Switch to implementation model** - I might switch over to Sonnet if I think the implementation part is straightforward. (Even with the more expensive [Anthropic Max Plan](https://www.anthropic.com/news/max-plan), I hit the rate limits for Opus sometimes).
  - Claude Code: `/model sonnet`
  - Cursor: Switch your model to Claude Sonnet 4 (or Gemini 2.5 is great too) in the model selector

- `Run @instructions/DO_PLANNING_DOC.md for [planning doc]`. Make a cup of tea. I have the Claude permissions mostly in YOLO mode, but it can't commit. The model will do a single stage (with lots of sub-actions), and then stop.

- It'll pause at the end of the stage, often waiting for approval on a commit message. Read the summary, do some manual testing, perhaps also `Run @instructions/DEBRIEF_PROGRESS.md`.

- **Continue iteration** - Clear context as above, then:
  - `Do next stage of planning doc, as per @instructions/DO_PLANNING_DOC.md`


- **Housekeeping** - Every so often:
  
  - Run `@instructions/UPDATE_HOUSEKEEPING_DOCUMENTATION.md`.
  
  - Run `@instructions/UPDATE_CLAUDE_INSTRUCTIONS.md`. I think it's probably important that `CLAUDE.md` (or some equivalent Cursor rules) includes important stuff, e.g. a summary of `instructions/CODING_PRINCIPLES.md`, project-specific coding guidelines, and `reference/DOCUMENTATION_ORGANISATION.md`). Then the prompts can be very short, and you can trust that the agent will find the right bit of the code reliably and without wasting too much context.
