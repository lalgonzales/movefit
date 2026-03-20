# Backend Integration (API Contract)

## Core endpoints

- GET `/measurements` (params: from, to, device_mac)
- POST `/measurements` (body: measurement payload)
- GET `/summary` (params: date-range)
- GET `/trends` (params: window: daily, weekly, monthly)
- GET `/alerts`, POST `/goals`

## Fetch example

```ts
import axios from 'axios';

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

export const getMeasurements = (params: Record<string, unknown>) => api.get('/measurements', { params });
```

## Auth / headers

- MVP stage: no auth.
- Later: JWT authorization header `Authorization: Bearer <token>`.
