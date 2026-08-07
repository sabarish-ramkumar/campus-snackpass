# Campus SnackPass — 2-Day Zero-to-Deployed Plan

Stack (chosen for speed, not flash):
- **Frontend**: React + Vite + Tailwind → deploy on **Vercel**
- **Backend**: Python + FastAPI + SQLAlchemy → deploy on **Render**
- **Database**: **Neon Postgres** (free, cloud, no local install — you use the same DB in dev and prod, so there's nothing to migrate later)

Why this combo: you already know Python, so FastAPI won't fight you. Neon means you never install or configure a database on your machine — one connection string, done. This is the single biggest time-saver in this plan.

You will produce, by the end: a working deployed app, a GitHub repo with clean commits, and a running log of every LLM prompt you use (required submission #2) — I'll tell you exactly what to save and when.

---

## DAY 1 — Environment + Full Frontend (2nd-year bar met by end of day)

### Session 0 — Machine setup (30–45 min)
**Install, in order:**
1. **Git** → https://git-scm.com/downloads. Verify: `git --version`
2. **Node.js LTS** → https://nodejs.org (LTS button). Verify: `node --version` and `npm --version`
3. **VS Code** → https://code.visualstudio.com. Install extensions: ESLint, Prettier, Tailwind CSS IntelliSense, Python
4. **Python** — you likely already have it for ML work. Verify: `python --version` (or `python3 --version`)
5. **GitHub account** if you don't have one, then in terminal:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   ```
6. Create an empty GitHub repo named `campus-snackpass` (public, no README/gitignore yet — you'll push from local).

**Common mistake:** installing Node via some random installer instead of nodejs.org — leads to permission errors later. Use the official LTS installer.

**Checklist:** ✅ git works ✅ node/npm work ✅ VS Code open ✅ empty GitHub repo exists

---

### Session 1 — Frontend scaffold (45–60 min)
**Learn:** what Vite does (dev server + bundler), what Tailwind's utility classes are, basic folder conventions in a React app.
**Why:** everything else sits on top of this.

**Steps:**
```bash
npm create vite@latest campus-snackpass -- --template react
cd campus-snackpass
npm install
```
Then set up Tailwind — run `npx tailwindcss init -p` if using Tailwind v3, or follow the exact Vite+Tailwind steps at https://tailwindcss.com/docs/installation (check current version, the setup command changes between major versions — trust the official docs page over any AI-remembered command here).

**Files to create:**
- `src/data/menuItems.js` — a static array of ~15 items: `{ id, name, category, price, description, image, tags }`
- `src/data/categories.js` — `["Beverages", "Snacks", "Meals", "Desserts"]`

**Test:** `npm run dev`, confirm the Vite starter page loads at `localhost:5173`.

**Git commit:** `chore: scaffold vite react project with tailwind`

**Checklist:** ✅ dev server runs ✅ Tailwind classes visibly work (test with a `bg-blue-500` div) ✅ static data files created

---

### Session 2 — Menu browse + category filter + search (2–3 hrs)
**Learn:** `useState`, conditional rendering, `.filter()` and `.includes()` on arrays, controlled inputs.
**Why:** this is core requirement #1 and #2.

**Files:**
- `src/components/MenuCard.jsx` — one item's display
- `src/components/CategoryFilter.jsx` — category buttons/tabs
- `src/components/SearchBar.jsx`
- `src/pages/Menu.jsx` — brings it together, holds `selectedCategory` and `searchTerm` state, derives the filtered list

**Logic pattern:**
```jsx
const filtered = menuItems.filter(item =>
  (selectedCategory === "All" || item.category === selectedCategory) &&
  item.name.toLowerCase().includes(searchTerm.toLowerCase())
);
```

**Test:** click each category, confirm only matching items show; type in search, confirm live filtering; combine both.

**Common mistake:** filtering by mutating the original array instead of deriving a new filtered list each render — causes stale UI.

**Git commit:** `feat: add menu browsing with category filter and search`

**Checklist:** ✅ all items render ✅ category filter works ✅ search works ✅ combining both works ✅ empty state shows when no matches

---

### Session 3 — Cart: add/remove/quantity (2–3 hrs)
**Learn:** lifting state up (or Context API if cart needs to be accessed from multiple places), array `.map()`/`.reduce()` for totals.
**Why:** core requirement #3.

**Decision:** for a project this size, **React Context** for cart state is enough — you don't need Redux/Zustand. Don't add a state library just to look impressive; a reviewer who knows better will see it as overkill.

**Files:**
- `src/context/CartContext.jsx` — `addItem`, `removeItem`, `updateQuantity`, `cartItems`
- `src/components/CartItem.jsx`
- `src/components/CartSummary.jsx` — live total via `reduce`

**Logic pattern:**
```jsx
const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
```

**Test:** add same item twice → quantity increments, doesn't duplicate row; remove → item disappears; total updates live on every change.

**Common mistake:** storing cart as a plain array of items instead of keyed by item id — makes quantity updates awkward and buggy.

**Git commit:** `feat: implement cart with add/remove/quantity and live total`

**Checklist:** ✅ add works ✅ remove works ✅ quantity +/- works ✅ total recalculates correctly ✅ cart persists while navigating between pages (not on refresh yet — that's fine)

---

### Session 4 — Checkout + order token generation (1–1.5 hrs)
**Learn:** simple ID generation, form basics.
**Why:** core requirement #4/#5 — this is what makes it feel like a real product, not a shopping list.

**Files:**
- `src/pages/Checkout.jsx` — order summary, confirm button
- `src/utils/generateToken.js`:
```js
export function generateOrderToken() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // no ambiguous chars like 0/O, 1/I
  let code = "";
  for (let i = 0; i < 5; i++) code += chars[Math.floor(Math.random() * chars.length)];
  return `SP-${code}`;
}
```
- `src/pages/OrderSuccess.jsx` — shows token big and clear, "show this at the counter" messaging

**Test:** complete a checkout, confirm token generates and displays, confirm cart clears after confirming.

**Git commit:** `feat: add checkout flow with order token generation`

**🎯 Checkpoint: at this point your app already satisfies every 2nd-year requirement end to end on static data. This is a legitimate, demoable milestone — don't skip celebrating it, and don't skip committing here.**

---

## DAY 2 — Backend, Database, Integration, Deployment (3rd-year bar)

### Session 5 — Backend scaffold + Neon setup (1–1.5 hrs)
**Learn:** what an ORM is, what a connection string is, basic FastAPI app structure.
**Why:** you need real persistence to satisfy the 3rd-year requirement — static data no longer counts.

**Steps:**
1. Go to https://neon.tech, sign up free, create a project, copy the connection string (looks like `postgresql://user:pass@host/dbname`).
2. In a new `backend/` folder:
```bash
mkdir backend && cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```
3. `backend/.env`:
```
DATABASE_URL=your_neon_connection_string_here
```
4. `backend/.gitignore`: add `venv/`, `.env`, `__pycache__/`

**Common mistake:** committing `.env` to GitHub with your real DB password in it. Double-check `.gitignore` before your first `git add`.

**Git commit:** `chore: scaffold fastapi backend and connect neon postgres`

---

### Session 6 — Models + seed data (1.5–2 hrs)
**Learn:** SQLAlchemy models, table relationships, running a script to insert data.

**Files:**
- `backend/app/models.py` — `MenuItem`, `Order`, `OrderItem` tables (see relationships below)
- `backend/app/database.py` — engine + session setup, reading `DATABASE_URL` from `.env`
- `backend/app/seed.py` — script that creates tables and inserts your ~15 menu items

**Relationships:**
```
MenuItem (id, name, category, price, description, is_active)
Order (id, token, status, total, created_at)
OrderItem (id, order_id → Order, menu_item_id → MenuItem, quantity, unit_price)
```
`unit_price` on `OrderItem` is copied from `MenuItem.price` **at order time** — this way if you ever change a menu price later, past orders' totals stay correct. This is worth mentioning if anyone asks about your schema design.

**Test:** run `python app/seed.py`, then check Neon's SQL editor (in their dashboard) to confirm rows exist.

**Git commit:** `feat: add sqlalchemy models and seed script`

---

### Session 7 — CRUD API endpoints (2–3 hrs)
**Learn:** FastAPI routing, Pydantic schemas (request/response validation), path/query params.

**Files:**
- `backend/app/schemas.py` — Pydantic models for request/response shapes
- `backend/app/main.py` — the FastAPI app + routes:
  - `GET /menu-items` (optional `?category=` filter)
  - `GET /menu-items/{id}`
  - `POST /orders` — accepts a list of `{menu_item_id, quantity}`, computes total server-side, generates token, saves
  - `GET /orders/{token}` — for order lookup

**Why compute total server-side, not trust the frontend's number:** never trust client-sent prices/totals — a user could tamper with the request. This is a real, specific thing to say in an interview if asked "how did you handle security."

**Test:** run `uvicorn app.main:app --reload`, open `localhost:8000/docs` (FastAPI's free auto-generated Swagger UI), test every endpoint there before touching the frontend.

**Git commit:** `feat: add CRUD API endpoints for menu items and orders`

---

### Session 8 — Connect frontend to backend (2 hrs)
**Learn:** `fetch` or `axios`, `useEffect` for data loading, loading/error states.

**Steps:**
1. `npm install axios` in frontend
2. Create `src/api/client.js` with an axios instance pointing at `http://localhost:8000` (use an env var so you can swap to the deployed URL later: `VITE_API_URL`)
3. Replace static `menuItems.js` imports with a `useEffect` fetch on the Menu page
4. Change checkout to `POST` to `/orders` instead of generating the token locally — **the backend now owns token generation**, since it also needs to guarantee uniqueness against the DB
5. Add a simple loading spinner and an error message state for failed requests

**Test:** full flow — browse (from DB) → filter → cart → checkout → real token from backend → confirm it matches what's in Neon.

**Common mistake:** CORS errors. If you see them, add FastAPI's `CORSMiddleware` in `main.py` allowing your frontend's origin.

**Git commit:** `feat: connect frontend to backend api, replace static data`

---

### Session 9 — Deployment (1.5–2 hrs)
**Backend → Render:**
1. Push backend to GitHub (or same repo, `backend/` subfolder)
2. On https://render.com: New → Web Service → connect repo → root directory `backend`
3. Build command: `pip install -r requirements.txt` (run `pip freeze > requirements.txt` first)
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable `DATABASE_URL` (your Neon string) in Render's dashboard — never in code

**Frontend → Vercel:**
1. On https://vercel.com: New Project → import your GitHub repo → root directory `campus-snackpass` (or wherever frontend lives)
2. Add environment variable `VITE_API_URL` = your Render backend URL
3. Deploy

**Test:** open the live Vercel URL, do a full order end to end, confirm it hits the live Render backend and writes to Neon.

**Common mistake:** forgetting to update CORS on the backend to allow your actual Vercel domain (not just `localhost`) — this bites almost everyone on first deploy.

**Git commit:** `chore: configure deployment env vars and CORS for production`

---

### Session 10 — README, LLM prompt log, final QA (1–1.5 hrs)
**Required submissions, both due:**

1. **GitHub repo** — make sure it has:
   - A real `README.md`: what the project is, tech stack, how to run locally, live demo link, screenshot
   - Clean commit history (you'll have one from every session above if you followed along)

2. **LLM prompts document** — this must be an honest record of prompts you actually used. Practical way to build it without extra work: as you go through Day 1–2, keep a running plain-text or Google Doc log — paste in the actual question you asked (me or any other AI tool) each time you asked for help, in order. At the end, export to PDF. Don't reconstruct this from memory at the very end — you'll forget half of it and it'll look thin. Start the doc now, right after this session plan, and add to it every time you ask something.

**Final QA pass:** test on a phone-sized browser window (responsive check), test an empty cart checkout attempt (should block, not crash), test searching for something that doesn't exist (empty state), refresh mid-flow (shouldn't hard-crash).

---

## If you run short on time

Cut in this order, not earlier ones: (1) search bar polish/animations, (2) multiple category tags per item, (3) order status beyond "pending". **Never cut**: the DB-backed CRUD, the live-deployed link, or the prompt log — those three are what's explicitly graded as required submissions.
