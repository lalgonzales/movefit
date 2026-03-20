# Frontend Team Guide: React + Vite + Tailwind

Objective: build the Movefit frontend client with a modern stack (React, Vite, Tailwind).

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
- `src/api/` Fetch/axios integrations for backend endpoints
- `src/lib/` utilities, date formatting, validators
- `src/styles/` tokens and Tailwind extensions

Approach:
- MVP first: ingestion + timeline + summary + goals
- API-friendly and feature flags (local/dev/production modes)
- testing: vitest + @testing-library/react + msw
