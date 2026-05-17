# Specs

Ralph Wiggum reads root-level Markdown files in this directory.

Topic-specific queues such as `mappers/` and `gymapi/` are planning backlogs.
Promote or copy one of those specs to this root directory, or explicitly target
it in the Ralph prompt, when it should become active loop work.

Use numeric prefixes to express priority:

```text
001-first-important-task.md
002-next-task.md
```

Each spec should include concrete acceptance criteria and verification commands. A spec is complete only when it contains:

```markdown
## Status: COMPLETE
```
