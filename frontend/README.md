# Cost Planner Frontend

Next.js-based wedding cost planner UI.

## Local Development

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

## Environment Variables

Copy `.env.local.example` to `.env.local` and configure:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Docker Build

```bash
docker build -t cost-planner-frontend ./frontend
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 cost-planner-frontend
```

## Features

- View all wedding cost plans
- Real-time budget tracking
- Responsive design
- Direct integration with Cost Planner API
