# extract.py
# Stage 1: pull live FX rates from the Frankfurter API and print them.

import requests   # the library that lets Python make web requests

# The API endpoint. We ask for rates with USD as the base currency.
# Frankfurter returns how much 1 USD is worth in each other currency.
API_URL = "https://api.frankfurter.dev/v1/latest?base=USD"


def fetch_rates():
    """Call the API and return the parsed data as a Python dictionary."""
    print(f"Requesting rates from: {API_URL}")

    response = requests.get(API_URL, timeout=10)   # send the GET request
    response.raise_for_status()                    # crash loudly if it failed

    data = response.json()   # turn the JSON response into a Python dict
    return data


def main():
    data = fetch_rates()

    # The response looks like:
    # {"amount": 1.0, "base": "USD", "date": "2026-06-20",
    #  "rates": {"EUR": 0.92, "GBP": 0.79, ...}}
    print(f"\nBase currency: {data['base']}")
    print(f"Rate date:     {data['date']}")
    print("\nSample rates:")

    for currency, rate in data['rates'].items():
        print(f"{currency} : {rate}")




if __name__ == "__main__":
    main()

