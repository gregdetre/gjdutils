This repo may be a specific project. But this task is about `gjdutils`, and sharing some of the techniques we're using here for AI-assisted programming.

Within it, we have cloned `gjdutils/` from https://github.com/gregdetre/gjdutils - this is my open source repository of useful scripts, snippets, and LLM prompts.

Every so often I would like to take a look at `docs/*.md`, and examine whether there are any docs in there that could usefully be ported over to `gjdutils/docs/` to be shared with the wider world.

I am actively improving & adding to `docs/` as I develop this project, and so I would like to occasionally update `gjdutils/docs/` to include improvements this project. The tricky part is that while some of the docs in this project's `docs/` are generic and could be of widespread utility (copied, perhaps with light modification to generalise them), some of the docs in this project's `docs/` are specific to this project, and it wouldn't make sense to include them in `gjdutils/docs/` (probably many of the ones in `docs/reference/`)

Gather information & compare what's in both `docs` folders, and then make a proposal for:
- Docs that exist in both that we should compare, and see if there are any improvements from one to port/update in the other (probably from `docs` -> `gjdutils/docs`, but perhaps occasionally vice versa), e.g.example `docs/WRITE_PLANNING_DOC.md` also exists as an older version as `gjdutils/docs/WRITE_PLANNING_DOC.md`.
- Docs that only exist in `docs/` and should be added to `gjdutils/docs` (or perhaps even vice versa).
- Docs that should be renamed in `gjdutils/docs` (because there's a better name in `docs/`).
- Docs that should be removed (though probably there should be a good reason for this, e.g. there are duplicates, or we agree the doc is bad/out of date in some clear way).
- Include this `docs/PORT_DOCS_TO_GJDUTILS.md` as an example of one we should port (so that other projects can also port their docs to become general/shareable)

When porting from `docs/` -> `gjdutils/docs/`, remove/generalise any references that are specific to this project. This could vary case-by-case, so let's discuss.

My guess is that many of the the most relevant docs will be commands (e.g. `WRITE_PLANNING_DOCS`, `DEBRIEF_PROGRESS.md`) or modes (e.g. `SOUNDING_BOARD_MODE.md`), etc.

Follow instructions in `TASKS_SUBAGENTS.md`.

Discuss your proposal with the user. Don't make changes until they have been agreed.

Once agreed, use tasks and subagents (provided with rich context) to make the updates.