# load.py
# Stage 2: fetch FX rates and load them into Postgres.

import requests
import psycopg2   # the Postgres driver

API_URL = "https://api.frankfurter.dev/v1/latest?base=USD"

# Connection details — these match the docker-compose.yml settings.
# Note host is localhost and port is 5433 (the port we exposed).
DB_CONFIG = {
    "host":     "localhost",
    "port":     5433,
    "dbname":   "insurance",
    "user":     "dataeng",
    "password": "dataeng_pass",
}


def fetch_rates():
    """Get the latest rates from the API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def load_rates(data):
    """Write each rate into the raw_fx_rates table."""
    base      = data["base"]
    rate_date = data["date"]
    rates     = data["rates"]

    # Open a connection to Postgres, then a cursor to run commands.
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    inserted = 0
    for currency, rate in rates.items():
        # This SQL inserts one row. The %s are placeholders that psycopg2
        # fills in safely — never build SQL by gluing strings together,
        # that's how SQL-injection bugs happen.
        #
        # ON CONFLICT ... DO NOTHING uses our UNIQUE constraint: if the
        # row for this (date, currency) already exists, skip it instead
        # of crashing. This makes the script safe to run repeatedly.
        cursor.execute(
            """
            INSERT INTO raw_fx_rates (base, rate_date, currency, rate)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (rate_date, currency) DO NOTHING
            """,
            (base, rate_date, currency, rate),
        )
        inserted += cursor.rowcount   # rowcount is 1 if inserted, 0 if skipped

    conn.commit()   # save the changes permanently
    cursor.close()
    conn.close()
    return inserted


def main():
    data = fetch_rates()
    print(f"Fetched {len(data['rates'])} rates for {data['date']}")

    count = load_rates(data)
     print(f"Inserted {count} new rows.")

    



if __name__ == "__main__":
    main()




