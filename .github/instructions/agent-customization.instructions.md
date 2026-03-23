---
name: movefit-agent-customization
description: "Guidance for creating or updating agent customization files and workspace instructions."
applyTo: "**/*.{md,yaml,yml}"
---

- For high-level workspace setup, use `.github/copilot-instructions.md` as the canonical source.
- Keep `AGENTS.md` updated with agent role summaries and recommended workflows.
- Add per-domain instruction files under `.github/instructions/` with `applyTo` glob patterns.
- Maintain tool restrictions and metadata in `.github/agents/<agent>.agent.md` per project conventions.
- Minimize duplication: prefer one definitive source for a policy rather than duplicating it across multiple agent files.
- When agent/skill/prompt/instructions content starts to feel “exaggerated”, do:
  - Group shared conventions in `.github/copilot-instructions.md` and `.github/instructions/agent-customization.instructions.md`.
  - Keep per-agent files small (role + tool boundaries + lifecycle notes).
  - Document a one-line “intended audience” header in each file (e.g., "coordination", "api feature", "testing").
- On new feature work, follow this workflow:
  1. Discover existing convention files (`.github/copilot-instructions.md`, `AGENTS.md`, relevant `movefit-*.instructions.md`).
  2. Explore code for architecture, tests, and existing patterns (e.g., `src/movefit`, `tests/`, `pyproject.toml`).
  3. Generate or merge: create new files only if needed; update existing with minimal drift and copy existing value.
  4. Iterate with reviewer feedback, then provide example prompts and next customization suggestions.
- Provide brief final responses with headings and markdown formatting.
