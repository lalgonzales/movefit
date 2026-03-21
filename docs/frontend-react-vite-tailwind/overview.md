# Frontend Team Guide: React + Vite + Tailwind for Movefit

Objective: build the Movefit frontend client with a modern stack.

Recommended dependencies:
- react 18+
- react-dom 18+
- vite 5+
- tailwindcss 4+
- postcss 8+
- autoprefixer 10+

Proposed architecture:
- `src/components/` common UI components
- `src/pages/` views (dashboard, measurements, goals, trends)
- `src/api/` backend client (axios or fetch)
- `src/lib/` utilities, date formatting, validators
- `src/styles/` tokens and Tailwind extensions

MVP focus:
- ingestion + timeline + summary + goals
- API-first, no authentication in initial milestone
- tests with vitest + @testing-library/react + msw
