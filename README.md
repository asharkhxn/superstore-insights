# Superstore Insights

A modern sales analytics dashboard built with **FastAPI**, **React**, **TypeScript**, and **Plotly**. Provides real-time insights into sales performance, profit trends, and customer segmentation.

## Demo

📹 [Watch Demo Video](https://drive.google.com/file/d/1SU_Zg88oj3JfdrLJRc6dOQoANYCUnVu3/view?usp=sharing)

## Features

- **Real-time KPIs**: Sales, profit, orders, customers, AOV, and profit margin
- **Interactive Charts**: Category distribution, regional performance, time-series trends, profit analysis, and customer segmentation
- **Geographic Visualization**: US state-level sales choropleth map
- **Advanced Filtering**: Date ranges, regions, segments, and product categories
- **Responsive Design**: Optimized for desktop and mobile devices

## Tech Stack

**Backend**

- FastAPI (Python 3.13)
- Pandas & PyArrow for data processing
- Plotly for server-side chart generation
- Pydantic for validation

**Frontend**

- React 18 + TypeScript
- Vite for fast builds
- Plotly.js for interactive charts
- Custom error handling with retry logic

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at: **http://localhost:8000**  
API Docs: **http://localhost:8000/docs**

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at: **http://localhost:5173**

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```

48 tests covering endpoints, data service, and chart generation.

### Frontend Tests

```bash
cd frontend
npm test
```

## Project Structure

```
superstore-insights/
├── backend/
│   ├── app/
│   │   ├── core/          # Config & dependencies
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   └── schemas/       # Response models
│   └── tests/
└── frontend/
    ├── src/
    │   ├── components/    # React components
    │   ├── hooks/         # Custom hooks
    │   └── types/         # TypeScript definitions
    └── test/
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/sales/overview` - KPI metrics
- `GET /api/sales/by-category` - Category analysis
- `GET /api/sales/by-region` - Regional breakdown
- `GET /api/sales/trends` - Time-series data
- `GET /api/sales/profit-analysis` - Profit metrics
- `GET /api/sales/by-segment` - Customer segmentation
- `GET /api/sales/geo-sales` - Geographic sales map
- `GET /api/sales/filter-options` - Available filter values
