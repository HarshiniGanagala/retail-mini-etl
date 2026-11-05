# Retail Mini ETL

A small, beginner-friendly Python project that cleans retail orders with pandas
and saves the results to CSV and SQLite.

## Run the project

Open a terminal in the project folder and run these commands.

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the ETL script

The script reads `data/raw/orders.csv`. If the file does not exist, it creates
30 example orders, including a few blank quantities. It fills blank quantities
with `1`, calculates revenue, then saves the cleaned orders to
`data/processed/orders_clean.csv` and the `orders_clean` table in
`db/orders.db`. It also prints the total orders, total revenue, and top product
by revenue.

```bash
python -m src.etl
```

### 4. Run the tests

```bash
python -m pytest
```

When you are finished, deactivate the virtual environment with:

```bash
deactivate
```
