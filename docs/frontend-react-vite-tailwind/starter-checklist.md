# Frontend Starter Checklist

1. Crear proyecto:
   - `npm create vite@latest movefit-frontend -- --template react`
2. Instalar Tailwind:
   - `npm install -D tailwindcss postcss autoprefixer`
   - `npx tailwindcss init -p`
3. Configurar `tailwind.config.js` y `src/index.css`
4. Instalar librerías de UX/UX:
   - `npm install axios react-router-dom`
5. Añadir linter/prettier:
   - `npm install -D eslint prettier eslint-config-prettier eslint-plugin-react`
6. Tests:
   - `npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event`
7. Estructura y convención:
   - `features/` para estado y hooks específicos
   - `api/` con contratos: `measurements.ts`, `goals.ts`, `alerts.ts`
   - `types/` para DTO shared con backend
8. Integración con backend (base URL env):
   - `.env` var `VITE_API_BASE_URL`.
