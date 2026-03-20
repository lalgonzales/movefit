# Frontend Starter Checklist

1. Create project:
   - `npm create vite@latest movefit-frontend -- --template react`
2. Install Tailwind:
   - `npm install -D tailwindcss postcss autoprefixer`
   - `npx tailwindcss init -p`
3. Configure `tailwind.config.js` and `src/index.css`
4. Install core libraries:
   - `npm install axios react-router-dom`
5. Add linter/prettier:
   - `npm install -D eslint prettier eslint-config-prettier eslint-plugin-react`
6. Tests:
   - `npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event`
7. Structure and conventions:
   - `features/` for feature state and hooks
   - `api/` with endpoint clients: `measurements.ts`, `goals.ts`, `alerts.ts`
   - `types/` for shared DTOs with backend
8. Backend integration (base URL env):
   - `.env` variable `VITE_API_BASE_URL`
