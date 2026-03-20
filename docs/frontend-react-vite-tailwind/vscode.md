# VSCode Setup for React + Vite + Tailwind (Movefit Frontend)

Recommended extensions:
- ESLint
- Prettier - Code formatter
- Tailwind CSS IntelliSense
- JavaScript (ES6) code snippets
- GitLens
- Vitest Runner / Jest Runner

Workspace settings (`.vscode/settings.json`):
- `editor.formatOnSave`: true
- `editor.codeActionsOnSave`: { "source.fixAll.eslint": true }
- `eslint.validate`: ["javascript", "typescript", "javascriptreact", "typescriptreact"]
- `tailwindCSS.includeLanguages`: { "plaintext": "html" }

Workspace files:
- `.vscode/extensions.json` with `recommendations`
- `.vscode/settings.json` with style and lint rules

Recommended commands:
- `npm run lint`
- `npm run format`
- `npm run test:watch`

Project paths:
- `src/api` backend service clients
- `src/features` feature state/data handling
- `src/components/ui` atomic UI components
