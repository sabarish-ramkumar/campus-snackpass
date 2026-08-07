# Campus SnackPass

A full-stack cafeteria pre-ordering app. Browse the menu, filter by category, search, build a cart, check out, and get a unique token to collect food — skipping the queue.

**Live demo:** _add your Vercel URL here after deploying_
**API docs:** _add your Render URL + `/docs` here after deploying_

## Tech Stack

- **Frontend:** React 19 + Vite + Tailwind CSS v4 + React Router v6, deployed on Vercel
- **Backend:** Python + FastAPI + SQLAlchemy 2.0, deployed on Render
- **Database:** Postgres (Neon)

## Features

- Browse menu, filter by category, live search (debounced)
- Cart with add / remove / quantity, live-updating total
- Checkout that generates a unique order token (e.g. `SP-4F2K9`) server-side
- Order lookup by token
- Full CRUD on menu items (create / read / update / soft-delete)

## Architecture notes worth knowing (in case you're asked)

- **Server-side price computation.** The frontend only ever sends `{ menu_item_id, quantity }` when placing an order. The backend looks up the real price and computes the total itself — a tampered request body can't change what gets charged.
- **Price snapshotting.** Each `order_items` row stores `unit_price` at the moment of purchase, separate from the live `menu_items.price`. Changing a menu price later doesn't retroactively change past order totals — verified directly: see the "price snapshot" test in the walkthrough this shipped with.
- **Soft delete on menu items.** Deleting a menu item sets `is_active = false` instead of removing the row, because past orders still reference it by foreign key.
- **CORS.** Frontend and backend are separate deployments (Vercel + Render), so CORS is configured explicitly rather than left open — see `backend/app/main.py`.

## Running locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your Neon DATABASE_URL
python -m app.seed              # populates menu_items, safe to re-run
uvicorn app.main:app --reload
```
API now running at `http://localhost:8000` — Swagger UI at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App now running at `http://localhost:5173`.

## Deployment

See `docs/2day-plan.md` (Session 9) for the full step-by-step Vercel + Render deployment guide, including environment variables and the CORS gotcha that trips up most first deploys.

## Known scope cuts (intentional, not oversights)

Given the assessment timeline, these were deliberately left out rather than half-built:
- No admin authentication on the CRUD endpoints (would be a JWT layer in front of the `/menu-items` write routes — straightforward to add, just cut for time)
- No QR code generation — token display was prioritized as the core requirement
- No Alembic migrations — `Base.metadata.create_all()` is used instead, which is fine at this scale but wouldn't be the right call on a team codebase with evolving schema

## LLM usage

Prompts used during development are logged in `llm-prompts.pdf` per the submission requirements.
