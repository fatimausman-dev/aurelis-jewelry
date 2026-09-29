# Jewelry Brand — Full Stack Setup

This zip contains the backend fully scaffolded, plus a `frontend-additions/`
folder you'll merge into your Next.js app after creating it (Next.js needs to
generate into a fresh directory, so we can't pre-zip the frontend itself).

Run every step below in order.

---

## 1. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Start Postgres + Redis (Docker)

```bash
docker run -d --name jewelry-postgres -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=jewelrybrand -p 5432:5432 postgres:16
docker run -d --name jewelry-redis -p 6379:6379 redis:7
```

Don't have Docker? Say so and we'll set up native Postgres/Redis instead.

**Stop here on the backend** — the .py files are empty placeholders. Don't run
`uvicorn` yet; there's nothing in them to serve.

---

## 3. Frontend setup

From the project root (one level above `backend/`):

```bash
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install framer-motion lucide-react
```

When prompted during `create-next-app`: say **yes** to `src/` directory and
App Router. ESLint is your call. Default import alias (`@/*`) is fine.

## 4. Merge in the additional folders/files

Copy everything from `frontend-additions/` into your new `frontend/` folder,
merging with what `create-next-app` already generated:

```bash
# from the project root
cp -r frontend-additions/src/* frontend/src/
cp -r frontend-additions/public/* frontend/public/
```

This adds:
- `src/app/shop`, `src/app/product/[id]`, `src/app/cart`, `src/app/checkout`,
  `src/app/order-confirmation/[id]`, `src/app/account` — the full purchase flow
- `src/components/splash/SplashScreen.tsx` — the intro overlay
- `src/components/hero`, `src/components/categories`, `src/components/products`,
  `src/components/layout` — page building blocks
- `src/lib/api.ts`, `src/lib/push.ts`, `src/lib/cart.ts` — backend calls, web
  push subscription, cart state
- `public/videos/`, `public/images/` — drop your hero video and category
  photos in here (see the README.txt in each folder)

## 5. Add your real assets

- Hero video → `frontend/public/videos/jewelry-hero.mp4`
- Splash screen product photo → `frontend/public/images/splash-ring.jpg`
- Category photos (8 total) → `frontend/public/images/category-*.jpg`
- Poster fallback → `frontend/public/images/jewelry-poster.jpg`

## 6. Run everything

```bash
# terminal 1
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# terminal 2
cd frontend && npm run dev
```

---

## Folder map (for reference)

```
jewelry-brand/
├── backend/
│   └── app/
│       ├── main.py, db.py, redis_client.py, config.py, schemas.py
│       ├── models/        product, order, customer, push_subscription
│       └── routers/       products, orders, auth, payments, stock_alerts
│
└── frontend/               (created by create-next-app, then merged)
    ├── src/
    │   ├── app/            page.tsx, shop, product/[id], cart, checkout,
    │   │                   order-confirmation/[id], account
    │   ├── components/     splash, hero, categories, products, layout
    │   └── lib/            api.ts, push.ts, cart.ts
    └── public/              videos/, images/
```

Next step once this is all running: I write the real code for
`SplashScreen.tsx`, the hero, and the product → cart → checkout chain.
