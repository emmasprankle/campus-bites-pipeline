# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery orders.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Setup

1. Clone the repo and navigate into it:
   ```bash
   git clone <your-repo-url>
   cd campus-bites-pipeline
   ```

2. Start the database:
   ```bash
   docker compose up -d
   ```

   On first run, Docker will create the `orders` table and load all 1,132 rows from the CSV automatically.

3. Verify it's running:
   ```bash
   docker ps
   ```

## Connect & Query

**Option 1 — psql (command line):**
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

**Option 2 — GUI (TablePlus, DBeaver, etc.):**
| Setting  | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5432         |
| Database | campus_bites |
| User     | postgres     |
| Password | postgres     |

## Example Queries

```sql
-- Preview the data
SELECT * FROM orders LIMIT 10;

-- Orders by cuisine type
SELECT cuisine_type, COUNT(*) AS total_orders
FROM orders
GROUP BY cuisine_type
ORDER BY total_orders DESC;

-- Average order value by customer segment
SELECT customer_segment, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY customer_segment
ORDER BY avg_value DESC;

-- Average delivery time by cuisine
SELECT cuisine_type, ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_mins
FROM orders
GROUP BY cuisine_type
ORDER BY avg_delivery_mins;
```

## Teardown

Stop the container (data is preserved):
```bash
docker compose down
```

Stop and delete all data:
```bash
docker compose down -v
```
