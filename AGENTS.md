# Movefit Custom Agent Definitions

This file documents project agents and how to use them.

## Agenda

- `movefit-coordinator`: high-level coordinator agent.
- `movefit-fastapi`: agent for API design/implementation (FastAPI + Pydantic + SQLModel).
- `movefit-data`: agent for calculations and metrics.
- `movefit-db`: agent for schema and persistence.
- `movefit-tests`: agent for unit and integration testing.
- `movefit-ci`: agent for CI pipeline and pre-commit.
- `movefit-git`: agent for git operations (commit/tag/push) from CI/coordinator workflows.
- `movefit-docs`: agent for documentation and design maintenance.

## Recommended usage

1. Start with `movefit-coordinator` to define feature strategy.
2. Use specialized subagents for each stage.
3. Validate output with `movefit-tests` and `movefit-ci`.
4. Update `docs/design.md` via `movefit-docs`.

## Agent metadata and standardization

- Cada agente tiene definición en `.github/agents/<agent>.agent.md` con frontmatter YAML.
- `tools:` debe limitarse a las capacidades requeridas por el rol (principio de menor privilegio).
- `user-invocable:` se fija en `true` solo para el coordinador y, opcionalmente, agentes de desarrollo manual.
- Cambios recientes: permisos de herramienta ajustados para cada agente según responsabilidad, y `movefit-git` no es invocable por usuario directo (desde el coordinador/CI).
- `movefit-git` usa staging explícito y commits de estilo Conventional Commits.
- Mantener `docs/design.md` actualizado con orquestación de agentes y flujo de trabajo esperado.
