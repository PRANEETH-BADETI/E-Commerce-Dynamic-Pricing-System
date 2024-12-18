import requests
import csv

# Your eBay App ID
APP_ID = "Praneeth-ProductS-PRD-a99edef9a-74fa11de"  # Replace with your eBay API key

# API endpoint
url = "https://svcs.ebay.com/services/search/FindingService/v1"

# Request headers
headers = {
    "X-EBAY-SOA-SECURITY-APPNAME": APP_ID,
    "Content-Type": "application/json"
}


# Function to flatten nested JSON objects
def flatten_json(nested_json, parent_key='', sep='_'):
    items = {}
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        elif isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                for i, sub_item in enumerate(v):
                    items.update(flatten_json(sub_item, f"{new_key}_{i}", sep=sep))
            else:
                items[new_key] = v
        else:
            items[new_key] = v
    return items


# List of search items to collect data for
search_items = ["laptop", "smartphone", "mouse"]  # Add more items as needed

# To store all unique fieldnames for CSV
all_fieldnames = set()

# Open CSV file for writing and set up CSV writer
with open("raw_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = None  # Writer will be initialized after we know the fieldnames
    for search_item in search_items:

        # Request parameters for the eBay API
        params = {
            "OPERATION-NAME": "findItemsByKeywords",
            "SERVICE-VERSION": "1.0.0",
            "SECURITY-APPNAME": APP_ID,
            "RESPONSE-DATA-FORMAT": "JSON",
            "REST-PAYLOAD": "",
            "keywords": search_item
        }

        # Make the request
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get("findItemsByKeywordsResponse", [{}])[0].get("searchResult", [{}])[0].get("item", [])

            # Flatten the item details
            flattened_items = [flatten_json(item) for item in items]

            # Update fieldnames to ensure new keys from each batch are added
            for item in flattened_items:
                all_fieldnames.update(item.keys())

            # Reinitialize writer to update the fieldnames if necessary
            if writer is None:
                writer = csv.DictWriter(file, fieldnames=sorted(all_fieldnames))
                writer.writeheader()  # Write header only once
            else:
                writer.fieldnames = sorted(all_fieldnames)  # Update fieldnames

            # Write data to the CSV file
            for item in flattened_items:
                # Write only the keys present in fieldnames to avoid ValueError
                row = {field: item.get(field, None) for field in writer.fieldnames}
                writer.writerow(row)
        else:
            print(f"Failed to fetch data for '{search_item}' (Status code: {response.status_code})")

print("Data has been successfully saved to 'raw_products.csv'.")
