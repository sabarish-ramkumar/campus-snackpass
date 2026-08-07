# Campus SnackPass

A full-stack cafeteria pre-ordering platform built to solve long queues during lunch rushes. Students can browse digital menus, filter by categories, search items live, build custom carts, and place orders to generate a unique pickup token for seamless queue-skipping collections.

---

## 🚀 Live Demo

* **Frontend App:** [campus-snackpass-app.vercel.app](https://campus-snackpass-app.vercel.app/)
* **Backend API:** [campus-snackpass.onrender.com](https://campus-snackpass.onrender.com)
* **Interactive API Docs (Swagger):** [campus-snackpass.onrender.com/docs](https://campus-snackpass.onrender.com/docs)

---

## 🛠️ Tech Stack

* **Frontend:** React 19, Vite, Tailwind CSS v4, React Router v6 (Deployed on **Vercel**)
* **Backend:** Python, FastAPI, SQLAlchemy 2.0, Pydantic (Deployed on **Render**)
* **Database:** PostgreSQL (Hosted on **Neon Database**)

---

## ✨ Features

* **Interactive Menu:** Filter by categories (*Beverages, Snacks, Meals, Desserts*) with debounced live search.
* **Smart Cart:** Dynamic quantity adjustment and real-time total updates.
* **Order Token Generation:** Server-side generation of short, secure order tokens (e.g., `SP-4F2K9`) for food collection.
* **Order Lookup:** Track order status and item breakdowns using the assigned order token.
* **Menu Management (CRUD):** Admin capability to create, read, update, and soft-delete menu items.

---

## 🏗️ Architecture & Key Engineering Decisions

* **Server-Side Price Calculation:** The frontend payload sends only item IDs and quantities (`{ menu_item_id, quantity }`). Total calculations occur exclusively on the backend to prevent request body price tampering.
* **Historical Price Snapshotting:** Each `order_items` record stores a frozen `unit_price` at the moment of purchase. Updating a menu item's price in the database does not retroactively alter past order historical totals.
* **Soft Deletes:** Deleting menu items sets `is_active = false` instead of executing a hard row deletion, maintaining foreign key integrity for historical orders.
* **Strict CORS Strategy:** Cross-Origin Resource Sharing is strictly configured between Vercel and Render to prevent unauthorized domain access.

---

## 💻 Local Setup & Development

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
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


## Known scope cuts (intentional, not oversights)

Given the assessment timeline, these were deliberately left out rather than half-built:
- No admin authentication on the CRUD endpoints (would be a JWT layer in front of the `/menu-items` write routes — straightforward to add, just cut for time)
- No QR code generation — token display was prioritized as the core requirement
- No Alembic migrations — `Base.metadata.create_all()` is used instead, which is fine at this scale but wouldn't be the right call on a team codebase with evolving schema

## LLM usage

Prompts used during development are logged in `llm-prompts.pdf` per the submission requirements.
