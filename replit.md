# Workspace

## Overview

pnpm workspace monorepo (TypeScript) + Python Streamlit app for BizPulse.

## Projects

### BizPulse Python (Primary — Streamlit)
- **Location**: `artifacts/bizpulse-python/`
- **Run**: `BizPulse Python` workflow (port 5000)
- **Stack**: Python 3.11, Streamlit, Plotly, Pandas, NumPy, RapidFuzz, NetworkX
- **Pages**: Platform Overview, Entity Resolution Engine, Business Directory, Officer Dashboard, Business Owner Portal
- **Engine modules**: `engine/entity_resolution.py`, `engine/anomaly_detection.py`
- **Mock data**: `data/mock_data.py`

### BizPulse React (Secondary — full-stack)
- **Location**: `artifacts/bizpulse/`
- **Stack**: React + Vite + Express API

### API Server
- **Location**: `artifacts/api-server/`
- **Routes**: /api/businesses, /api/alerts, /api/resolve, /api/stats, /api/sector-analytics

## Python Stack (BizPulse)
- **UI**: Streamlit
- **Charts**: Plotly
- **Entity Resolution**: RapidFuzz (fuzzy matching + PAN cross-reference)
- **Anomaly Detection**: NumPy/Pandas z-score time-series analysis
- **Data**: In-memory mock data (simulates federated Karnataka govt databases)

## Node/TypeScript Stack
- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)

## Key Commands
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks/Zod schemas
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
