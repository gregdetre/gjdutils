These Cursor rules need to copied or symlinked to /your/project/.cursor/rules/

To include all of them, run this in your current project root dir:

```
mkdir -p .cursor/rules
ln -s "/path/to/gjdutils/.cursor/rules" ".cursor/rules/gjdutils_rules"
```

These `gjdutils` rules are mostly generic, though @testing-python.mdc and @writing-planning-docs.mdc reference specific paths.

These rules have all been marked as manual. You may want to define how they'll be applied for your project.

My current approach is to create lots of small rules and explicitly reference one or more of them explicitly, but I'm sure this will evolve over time.

e.g.

- Debug problem X, following @scientistic-detective.mdc

- Do X, following @coding.mdc @sounding-board.mdc @testing-python.mdc

- Write a planning doc for X, following @writing-planning.mdc