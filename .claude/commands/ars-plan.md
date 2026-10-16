---
disable-model-invocation: true
name: ars-plan
description: ARS academic-paper `plan` mode — Socratic chapter-by-chapter planning
model: sonnet
---

First invoke the Skill tool with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `plan` mode. Produces a Chapter Plan + INSIGHT collection through Socratic dialogue with the user. Originality-spectrum, very-high oversight.

Mode reference: `.claude/skills/MODE_REGISTRY.md` § academic-paper.
Skill entry: `.claude/skills/academic-paper/SKILL.md`.

Resolve plugin resources from `.claude/skills`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
