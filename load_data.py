import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# --- Configuration ---
# Connection details for the local Postgres container defined in docker-compose.yml
DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# Path to the source CSV file, relative to the project root
CSV_PATH = "data/campus_bites_orders.csv"

# --- Table definition ---
# IF NOT EXISTS means this is safe to run against an existing database —
# it won't fail or overwrite data if the table already exists
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     TEXT,
    is_reorder          TEXT
);
"""

# --- Load CSV ---
# pandas infers column types automatically from the CSV contents
df = pd.read_csv(CSV_PATH)

# --- Connect to Postgres ---
# ** unpacks the DB dict as keyword arguments to psycopg2.connect()
conn = psycopg2.connect(**DB)
cur = conn.cursor()

# --- Create table ---
cur.execute(CREATE_TABLE)

# --- Insert rows ---
# Convert the DataFrame to a list of plain tuples, one per row
rows = list(df.itertuples(index=False, name=None))

# execute_values inserts all rows in a single batch, which is much faster
# than looping and inserting one row at a time.
# ON CONFLICT DO NOTHING skips any row whose order_id already exists,
# making the script safely re-runnable without duplicating data.
execute_values(
    cur,
    """
    INSERT INTO orders (
        order_id, order_date, order_time, customer_segment,
        order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder
    ) VALUES %s
    ON CONFLICT (order_id) DO NOTHING
    """,
    rows,
)

# --- Commit and close ---
# commit() writes the transaction to the database; without it, inserts are rolled back
conn.commit()
cur.close()
conn.close()

print(f"Loaded {len(rows)} rows into orders.")
