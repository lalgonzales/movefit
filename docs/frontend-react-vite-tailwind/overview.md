# Frontend Team Guide: React + Vite + Tailwind

Objetivo: crear la app de cliente para Movefit con stack moderno (React, Vite, Tailwind). 


dependencias recomendadas:
- react 18+
- react-dom 18+
- vite 5+
- tailwindcss 4+
- postcss 8+
- autoprefixer 10+

Arquitectura propuesta:
- `src/components/` UI genéricos
- `src/pages/` vistas (dashboard, measurements, goals, trends)
- `src/api/` servicios Fetch/axios para endpoints backend
- `src/lib/` utilidades, formatos de fecha, validadores
- `src/styles/` tokens y extensiones Tailwind

Enfoque:
- MVP first: ingesta + timeline + resumen + objetivos
- API friendly y feature flags (modo local/dev/production)
- pruebas: vitest + @testing-library/react + msw
