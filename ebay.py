import requests
import csv

# Replace with your eBay Production App ID
APP_ID = "Praneeth-ProductS-PRD-a99edef9a-74fa11de"

# API endpoint
url = "https://svcs.ebay.com/services/search/FindingService/v1"

# Request headers and parameters
headers = {
    "X-EBAY-SOA-SECURITY-APPNAME": APP_ID,
    "Content-Type": "application/json"
}
# Function to get data from eBay API
def get_ebay_data(keywords):
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": keywords
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        items = data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
    except KeyError:
        print(f"No items found for {keywords}")
        return []

    result = []
    for item in items:
        title = item.get("title", ["N/A"])[0]
        primary_category = item.get("condition_0_conditionDisplayName", [{}])[0]
        category_id = primary_category.get("categoryId", "N/A")
        category_name = primary_category.get("categoryName", "N/A")
        selling_status = item.get("sellingStatus", [{}])[0]
        current_price = selling_status.get("currentPrice", [{}])[0]
        price = current_price.get("__value__", "N/A")
        currency = current_price.get("@currencyId", "N/A")
        condition_info = item.get("condition", [{}])[0]
        condition_name = condition_info.get("conditionDisplayName", "N/A")
        location = item.get("location", ["N/A"])[0]
        shipping_info = item.get("shippingInfo", [{}])[0]
        shipping_cost_info = shipping_info.get("shippingServiceCost", [{}])[0]
        shipping_cost = shipping_cost_info.get("__value__", "N/A")
        shipping_type = shipping_info.get("shippingType", ["N/A"])[0]
        url_1 = item.get("viewItemURL", ["N/A"])[0]
        result.append([
            item_id, title, category_id, category_name, price, currency,
            condition_name, location, shipping_cost, shipping_type, url_1
        ])  # Add 'keywords' as the Category column
    return result


# # Make the request
# response = requests.get(url, headers=headers, params=params)
# data = response.json()
#
# # Extract items
# items = data["findItemsByKeywordsResponse"][0]["searchResult"][0].get("item", [])

categories = ["Smartphones", "Laptops", "Tablets", "Earbuds", "keyboard", "Mouse"]

# Save data to CSV
with open("final_products.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Item ID", "Title", "Category ID", "Category Name", "Price", "Currency",
        "Condition", "Location", "Shipping Cost", "Shipping Type", "URL"
    ])
    for category in categories:
        data = get_ebay_data(category)
        if data:
            writer.writerows(data)

print("Data has been successfully saved to 'final_products.csv'.")

