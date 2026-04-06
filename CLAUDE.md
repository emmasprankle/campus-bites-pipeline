# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Database

Postgres 16 runs in Docker. The database is named `campus_bites`, credentials are `postgres/postgres`, port `5432`.

```bash
# Start the database
docker compose up -d

# Stop (data preserved)
docker compose down

# Stop and wipe all data (forces re-load on next start)
docker compose down -v
```

Connect via psql:
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

Run a non-interactive query:
```bash
docker exec campus_bites_db psql -U postgres -d campus_bites -c "SELECT COUNT(*) FROM orders;"
```

## Data loading

`load_data.py` creates the `orders` table (if it doesn't exist) and bulk-loads `data/campus_bites_orders.csv` using psycopg2. It is idempotent — re-running it skips rows that already exist via `ON CONFLICT (order_id) DO NOTHING`.

```bash
source .venv/bin/activate
python load_data.py
```

To reset and reload from scratch:
```bash
docker compose down -v && docker compose up -d
python load_data.py
```

## Python environment

Python 3.12 virtual environment at `.venv/`. Dependencies: `pandas`, `psycopg2-binary`.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## GUI connection

Connect with TablePlus, DBeaver, or similar:

| Setting  | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5432         |
| Database | campus_bites |
| User     | postgres     |
| Password | postgres     |

## Architecture

This is a single-table analytics database. The entire dataset lives in one table:

**`orders`** — 1,132 rows of campus food delivery orders with fields: `order_id`, `order_date`, `order_time`, `customer_segment`, `order_value`, `cuisine_type`, `delivery_time_mins`, `promo_code_used`, `is_reorder`.

**Schema note:** `promo_code_used` and `is_reorder` are stored as `TEXT`, not booleans. Filter them with string literals: `WHERE promo_code_used = 'Yes'`.

The data flow is: `data/campus_bites_orders.csv` → `load_data.py` → `orders` table in Postgres. There is no `init.sql`; all schema creation and loading is handled by `load_data.py`. The `./data` directory is also volume-mounted inside the container at `/data`.
