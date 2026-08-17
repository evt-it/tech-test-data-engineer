# Senior Data Engineer - Technical Assessment

## Overview

This test is designed to be completed in around 3 hours. You have one week - there is no time pressure, but we expect a focused, production-quality submission rather than an exhaustive one.

You are welcome to use AI tooling. We review your commit history to understand how you approached the problem - commit at logical milestones (e.g. Bento config, Dockerfile, Dagster asset, schedule, S3 export) rather than a single final commit.

---

## The Stack

The scaffold provides a fully working local environment. You are not expected to modify it beyond the tasks below. All service images are version-pinned - please do not change them.

| Service | Image | Description |
|---|---|---|
| `event-source` | (provided) | Python HTTP service serving sales events |
| `postgres` | `postgres:18` | Sales database pre-seeded with 100 historical orders |
| `dagster` | custom image - Dagster `1.13.8` | Dagster webserver + daemon (`http://localhost:3000`) |
| `garage` | `dxflrs/garage:v2.3.0` | S3-compatible local object storage |

The Dagster image has these Python libraries pre-installed for your use: `boto3`, `psycopg2-binary`, `pandas`. If you need anything else, add it to `dagster/Dockerfile` and note why in `NOTES.md`.

For Task 1 you will add a Bento service yourself - pin it to `ghcr.io/warpstreamlabs/bento:1.18`.

---

## Prerequisites

- Docker and Docker Compose
- Python 3.10+

---

## Getting Started

This repository is public, so a plain "Fork" would stay public too. Instead, make a genuinely private copy:

1. Go to [github.com/new/import](https://github.com/new/import).
2. Paste this repository's URL as the source, give it a name, and set visibility to **Private**.
3. Clone your new private repository and work directly in it.

```bash
git clone <your-private-repo-url>
cd tech-test
docker compose up
```

Commit regularly at logical milestones as you go (e.g. Bento config, Dockerfile, Dagster asset, schedule, S3 export) rather than one final commit at the end - see [Submission](#submission).

Verify the stack is running:

- Dagster UI: `http://localhost:3000`
- Event source: `http://localhost:8000/event`
- S3 storage - Garage has no web console; verify with the AWS CLI:

```bash
AWS_ACCESS_KEY_ID=GKtechtest0000000000000000 \
AWS_SECRET_ACCESS_KEY=techtest-secret-key \
aws s3 ls s3://reports \
  --endpoint-url http://localhost:3900 \
  --region garage
```

(An empty result is expected on a fresh stack - the bucket exists but has no objects yet. An error means something is wrong.)

> If any service fails to start, check `docker compose logs <service-name>`.

---

## Connection Details

All values below are injected into containers on the Compose network as environment variables (see the `x-connection-env` block in `docker-compose.yml`) - your code and configs should read them from the environment rather than hardcoding them. For this exercise, Compose-provided environment variables are sufficient; no secrets manager is expected.

| Environment variable | Value |
|---|---|
| `POSTGRES_HOST` | `postgres` |
| `POSTGRES_PORT` | `5432` |
| `POSTGRES_DB` | `sales` |
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| `EVENT_SOURCE_URL` | `http://event-source:8000/event` |
| `S3_ENDPOINT_URL` | `http://garage:3900` |
| `S3_REGION` | `garage` |
| `S3_BUCKET` | `reports` |
| `AWS_ACCESS_KEY_ID` | `GKtechtest0000000000000000` |
| `AWS_SECRET_ACCESS_KEY` | `techtest-secret-key` |

From your host machine (outside the Compose network), use `localhost` with the same ports: Postgres on `localhost:5432`, the event source on `localhost:8000`, S3 on `localhost:3900`.

> **Important:** Garage requires the region `garage` and path-style addressing. With boto3, configure the client with `endpoint_url`, `region_name="garage"`, and `Config(s3={"addressing_style": "path"})`. Skipping this produces opaque signature errors.

### Event Source

```
GET http://localhost:8000/event
```

Each GET request returns exactly one new JSON sales event. Every event carries a freshly generated UUID `order_id` - events are unique and the endpoint never emits duplicates. Your pipeline should poll this endpoint on a ~2-second interval.

---

## Data Dictionary

### `sales.orders` - pre-seeded table

The table is seeded with **100 historical orders** (timestamps in the past) so you can develop and test your SQL immediately. Fresh rows only appear once your Task 1 pipeline is running - see the Task 2 asset check.

| Column | Type | Description |
|---|---|---|
| `order_id` | `UUID` | Unique order identifier |
| `customer_id` | `UUID` | Customer identifier |
| `product_id` | `VARCHAR` | Product SKU |
| `product_name` | `VARCHAR` | Product display name |
| `category` | `VARCHAR` | Product category |
| `quantity` | `INTEGER` | Units ordered |
| `unit_price` | `NUMERIC(10,2)` | Price per unit at time of order |
| `total_amount` | `NUMERIC(10,2)` | `quantity × unit_price` |
| `order_ts` | `TIMESTAMPTZ` | Event timestamp (UTC) |

### Event Source Payload

Each HTTP response returns a single event in this shape:

```json
{
  "order_id": "a1b2c3d4-...",
  "customer_id": "e5f6...",
  "product_id": "SKU-001",
  "product_name": "Wireless Headphones",
  "category": "Electronics",
  "quantity": 2,
  "unit_price": 79.99,
  "total_amount": 159.98,
  "order_ts": "2025-01-15T10:23:45Z"
}
```

---

## Your Tasks

The two tasks form one end-to-end pipeline: **ingest events → land in Postgres → produce an automated daily category report in S3.** They can be developed in parallel (the seed data supports Task 2 development), but a complete submission requires both running together.

### Task 1 - Bento Pipeline

Build a Bento pipeline that continuously reads from the event source HTTP endpoint and writes each event to the `sales.orders` table in Postgres.

**Deliverable:** A `Dockerfile` (based on `ghcr.io/warpstreamlabs/bento:1.18`) that packages your Bento config so it runs as a container within the Docker Compose network. Add it as a service in `docker-compose.yml`.

The Bento container must:
- Poll `http://event-source:8000/event` on a ~2-second interval
- Parse the JSON payload
- Write each event to `sales.orders`
- Read connection details from environment variables

**Reference:** [Bento documentation](https://warpstreamlabs.github.io/bento/) · [Bento on GitHub](https://github.com/warpstreamlabs/bento)

---

### Task 2 - Dagster Asset & Schedule

Build a Dagster asset in `dagster_project/assets/` that answers the following business question, and schedule it to run daily.

> **What is the total revenue and total units sold per product category?**

The asset must:

1. **Asset check (freshness)** - verify that `sales.orders` contains at least one row with `order_ts` within the **last 10 minutes**. Fail with a clear message if not. (This check passes only when your Task 1 pipeline is running - the seed data alone will not satisfy it.)
2. **Query** - run a single SQL query against Postgres that produces revenue and units sold per category, ordered by total revenue descending.
3. **Materialise** - include materialisation metadata reporting the row count of the result.
4. **Export** - write the result as a CSV to the `reports` S3 bucket with the key `category_summary/YYYY-MM-DD.csv` using today's date **in UTC**.
5. **Schedule** - define a Dagster schedule that materialises the asset **daily at 09:00 UTC**, so the report is produced automatically. The schedule must be enabled **in code** (e.g. `default_status=DefaultScheduleStatus.RUNNING`) so it is active on a fresh `docker compose up`. Enabling it only via the UI toggle is stored in local instance state, not in your repository - it will not survive a fresh clone and will be assessed as not enabled.

**Scaffold note:** The Dagster container mounts `dagster_project/` as a volume. Register your asset, asset check, and schedule in `dagster_project/definitions.py` (the file contains a worked example) and they will be picked up automatically - no image rebuild required. After editing, use **Reload definitions** in the Dagster UI.

---

### Task 3 - Production Readiness (written, in `NOTES.md`)

In `NOTES.md`, briefly answer (aim for half a page total):

> If this pipeline were deployed to production, what would you change or add? Consider failure handling, observability, data quality, and deployment - and what you would deliberately *not* build yet.

We are looking for judgement and prioritisation, not an exhaustive list.

---

## Submission

1. Work in your private copy - do **not** make it public.
2. Commit at logical milestones - we review your git history to understand your approach.
3. Grant read access to `evt-jacob-roe` and `evt-rohit-naik` on your repository so we can review it.
4. When finished, email **jacob_roe@evt.com** with a link to your repository, confirming it's ready for review.

> **How we review:** we clone your repository and run `docker compose up` from scratch. Anything configured only through the Dagster UI (schedule toggles, run history, materialisations) lives in local instance state and is not part of your submission - everything must work from a clean clone.

Your repo should contain at minimum:

```
bento/
  Dockerfile
  config.yaml          # or equivalent
dagster_project/
  assets/
    sales_summary.py   # or equivalent
NOTES.md
```

Use `NOTES.md` for Task 3 plus anything you want to flag - assumptions made, things you would do differently with more time, or known limitations.

---

## What We Are Looking For

| Area | What good looks like |
|---|---|
| Bento config | Correct input/output wiring, clean YAML, handles the polling pattern |
| Dockerfile | Minimal image, config correctly packaged, integrates with the Compose network |
| Dagster | Correct use of Dagster primitives - asset, asset check, schedule, materialisation metadata |
| SQL | Correct aggregation, readable query |
| S3 integration | Correct use of the S3 API, sensible key structure, correct Garage client configuration |
| Code quality | Readable, no dead code, connection details read from environment variables (the Compose-provided values - no secrets manager expected) |
| Production thinking | NOTES.md shows pragmatic judgement about what production-readiness requires |
| Git hygiene | Meaningful commit messages, logical progression |

We are not looking for over-engineering. A clean, working solution is better than an ambitious incomplete one.

---

## Questions

If anything in the scaffold is not working as described, contact **jacob_roe@evt.com** - we want to eliminate environment issues as a variable.

---

*This assessment is confidential. Please do not share the repository, its contents, or your solution publicly.*
