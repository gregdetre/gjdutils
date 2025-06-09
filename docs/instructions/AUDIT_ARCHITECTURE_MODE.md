# Architecture‐Audit Mode

## Introduction
A lightweight, repeatable process for performing quick code-base audits that focus on robustness and flexibility of foundations rather than feature delivery or production hardening.

This mode is intended for moments when we pause feature work to check our architectural hygiene and coding style. It guides what to look for, how to stage improvements, and how to capture the findings in planning docs.

## See also
- `docs/WRITE_EVERGREEN_DOC.md` – conventions for evergreen documentation like this file.
- `docs/WRITE_PLANNING_DOC.md` – how to record stage-based action plans (used by the Appendix we add to planning docs).
- Example planning docs with `Appendix – recommendations from another AI – foundations focus` sections generated via this mode.

## Audit Workflow
1. **Scan** the target area (component, API route, service) for non-determinism, silent failures, and coupling.
2. **Record findings** in the relevant planning doc under a new appendix section (prefix with "(Discuss with the user …)"). Make sure you provide enough detail for someone else to successfully implement
3. **Prioritise** findings into stages (A, B, C…) with task lists following `WRITE_PLANNING_DOC.md`.
4. **Implement** each stage sequentially, ensuring tests pass after every stage. Commit with messages per `docs/GIT_COMMITS.md`.
5. **Update documentation** – if a pattern is generally useful, refine this evergreen doc.

## Maintenance
Review this doc quarterly or whenever we notice repeated architectural hygiene issues. Keep examples current and cross-references valid.
