# Superstore Insights

A full-stack sales analytics dashboard built with **FastAPI + React + TypeScript + Plotly**.

## Features

- KPI overview (sales, profit, orders, customers, AOV, profit margin)
- Interactive charts (category, region, trends, profit, segment)
- Global filters (date range, region, segment, category)

## Run locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173

## Tests (optional)

Backend:

```bash
cd backend
source venv/bin/activate
pytest
```

Frontend:

```bash
cd frontend
npm test
```

# superstore-insights

Full-stack analytics app for the Superstore dataset, built with FastAPI and React. Focused on clear, reliable data processing, server-side Plotly charts, and production-lean engineering practices.
