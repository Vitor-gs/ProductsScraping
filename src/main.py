#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests==2.32.3", "beautifulsoup4==4.13.4"]
# ///
import json
import random
import requests
import traceback
from bs4 import BeautifulSoup
from mapper import ProductMapper


PRODUCTS_TO_SCRAPE = [69, 25, 16, 24, 23, 18, 20, 19, 21, 26, 145, 13, 213]  # Selected AC and DC Motors types
DEMO = True  # If True, scrape only one product per selected category (total: 13 products)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}
session = requests.Session()
session.headers = headers
print("Starting scraping process...", flush=True)

try:
    for category in PRODUCTS_TO_SCRAPE:
        # Gets the total number of products in each category
        url = (f"https://www.baldor.com/api/products?include=results"
               f"&language=en-US"
               f"&pageIndex=0"
               f"&pageSize=1"
               f"&category={category}")
        response = session.get(url)
        total = response.json()["results"]["count"]
        random.seed(12)
        page_index = random.randint(0, total - 1) if DEMO else 0
        page_size = 1 if DEMO else total

        # If DEMO is True, extract data from one random product
        # If DEMO is False, extract data from all products
        url = (f"https://www.baldor.com/api/products?include=results"
               f"&language=en-US"
               f"&pageIndex={page_index}"
               f"&pageSize={page_size}"
               f"&category={category}")
        response = session.get(url)
        for product_data in response.json()["results"]["matches"]:
            product_id = product_data["code"]
            product_category = ";".join([c["text"] for c in product_data["categories"]]) if product_data["categories"] else None

            url = f"https://www.baldor.com/catalog/{product_id}"
            print(f"Extracting data from: {product_id}", flush=True)
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            product_details = soup.find("div", attrs={"id": "catalog-detail"})
            mapper = ProductMapper(product_id, product_category, product_details, session)
            product = mapper.get_product()
            with open(f"./output/{product_id}.json", "w") as f:
                json.dump(product, f)
    print("Process completed successfully!", flush=True)
except Exception as ex:
    print(f"[ERROR] {ex}", flush=True)
    traceback.print_exc()
finally:
    session.close()
