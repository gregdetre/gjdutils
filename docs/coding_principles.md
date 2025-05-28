# Coding Principles

## Core Philosophy
- Prioritise code that's simple, easy-to-understand, debuggable, and readable
- Fix the root cause rather than putting on a band-aid
- Avoid fallbacks & defaults - better to fail if input assumptions aren't being met

## Error Handling
- Raise errors early, clearly & fatally
- Prefer not to wrap in try/except so that tracebacks are obvious

## Development Approach
- Don't try to write a full, final version immediately
- Get a simple version working end-to-end first, then gradually layer in complexity in stages
- Aim to keep changes minimal and focused on the task at hand
- Try to keep things concise, don't over-engineer

## Best Practices
- Follow software engineering best practices:
  - Reuse code where it makes sense
  - Pull out core reusable functionality into utility functions
  - Break long/complex functions down
- Write code that's easy to test, prefer functional style
- Avoid object-oriented unless it's a particularly good fit
- Keep documentation up-to-date as you go

## Collaboration
- If the user asks you a question, answer it directly, and stop work on other tasks until consensus has been reached
- If you notice other things that should be changed/updated, ask/suggest
- If things don't make sense or seem like a bad idea, ask questions or discuss rather than just going along with it
- Be a good collaborator and help make good decisions, rather than just obeying blindly

## External Dependencies
- When picking 3rd-party libraries, prefer ones with large communities

## Comments
- Comment sparingly - reserve it for explaining surprising or confusing sections