# Commit Message Guidelines (Conventional Commits)

Para que Copilot y el flujo de CI mantengan un historial legible y utilizable, seguimos el estándar Conventional Commits:

Formato:
```txt
<type>(<scope>): <subject>

<body>

<footer>
```

Tipos comunes:
- feat: nueva funcionalidad
- fix: corrección de bug
- docs: cambios en documentación
- style: formato/código sin lógica
- refactor: reestructura sin comportamiento nuevo
- perf: mejoras de rendimiento
- test: adición/corrección de tests
- chore: tareas de mantenimiento

Reglas básicas:
- `subject` en presente y modo imperativo, max 72 caracteres.
- `body` explicativo si se necesita contexto ampliado (72 chars wrap).
- `footer` para tickets o BREAKING CHANGE.
- Usa `git add -p`/`git add <files>`; evita `git add .`.

Ejemplo:
```txt
feat(measurement): add csv bulk import endpoint

Implementa endpoint POST /measurements/bulk-import con validación de filas.

Closes #43
```
