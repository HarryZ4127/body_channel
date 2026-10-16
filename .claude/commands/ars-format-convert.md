---
disable-model-invocation: true
name: ars-format-convert
description: ARS academic-paper `format-convert` mode — convert to LaTeX / DOCX / PDF / Markdown
model: sonnet
---

First invoke the Skill tool with `skill: "academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `format-convert` mode. Converts a paper between LaTeX, DOCX (via Pandoc), PDF, or Markdown, and converts citation styles between major formats. Fidelity spectrum, low oversight.

Mode reference: `.claude/skills/MODE_REGISTRY.md` § academic-paper.
Skill entry: `.claude/skills/academic-paper/SKILL.md`.

Resolve plugin resources from `.claude/skills`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
