# Academic Research Skills (ARS), vendored

Source: https://github.com/Imbad0202/academic-research-skills @ 4c54490 (v3.23.1)
Author: Cheng-I Wu. License: CC-BY-NC-4.0 (see `skills/LICENSE`, `skills/NOTICE.md`).

Copied here so cloud sessions on this repo load ARS without the plugin installed.

Layout:
- `skills/` is the ARS plugin root (what `${CLAUDE_PLUGIN_ROOT}` pointed to); the 5 skills
  plus `shared/`, `scripts/`, `docs/`, `examples/`, `MODE_REGISTRY.md`.
- `commands/ars-*.md` are the plugin's slash commands, rewritten to load the unprefixed
  skill names and `.claude/skills/...` paths.
- `agents/` are the plugin's 4 subagents.

Left out: upstream tests, evals, plugin-evals, audits, translated READMEs, CI config.
The plugin's hooks (SessionStart banner, PreToolUse write-scope guard) are not enabled.

To update: re-copy from a newer upstream checkout and redo the
`${CLAUDE_PLUGIN_ROOT}` -> `.claude/skills` rewrite in the Markdown files.
