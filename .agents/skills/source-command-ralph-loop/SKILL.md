---
name: "source-command-ralph-loop"
description: "Run the Ralph Wiggum loop for a spec (Codex)"
---

# source-command-ralph-loop

Use this skill when the user asks to run the migrated source command `ralph-loop`.

## Command Template

Use this command to run an autonomous Ralph loop for a spec:

```
/ralph-loop:ralph-loop "Implement spec {spec-name} from specs/{spec-name}/spec.md.
Complete ALL Completion Signal requirements.
Output <promise>DONE</promise> when complete." --completion-promise "DONE" --max-iterations 30
```
