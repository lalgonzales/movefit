# Backend Integration (API Contract)

## Endpoints principales

- GET `/measurements` (filtros: from, to, device_mac)
- POST `/measurements` con body de lectura
- GET `/summary` (param date-range)
- GET `/trends` (param window: daily/weekly/monthly)
- GET `/alerts` y POST `/goals`

## Ejemplo fetch

```ts
import axios from 'axios';
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

export const getMeasurements = (params) => api.get('/measurements', { params });
```

## Auth / headers

- Inicialmente sin auth (MVP), luego JWT Authorization header `Bearer <token>`.
