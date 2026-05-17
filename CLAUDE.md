# Agent Instructions

Read `.specify/memory/constitution.md` first. It is the source of truth for project goals, submodule boundaries, Ralph Wiggum workflow rules, autonomy settings, and completion signals.

## Quick Reference

You are in a Ralph loop if you were started by `scripts/ralph-loop*.sh`, the prompt mentions implementing specs, or the prompt asks you to work through the queue autonomously.

In a Ralph loop, pick the highest priority incomplete spec from `specs/`, implement it completely, verify acceptance criteria, commit and push child submodule changes first, commit and push the umbrella submodule pointer second, then output `DONE`.

In interactive chat, help the user design specs, maintain the umbrella setup, or make requested changes normally.
