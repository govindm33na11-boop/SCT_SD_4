import csv
import requests
from bs4 import BeautifulSoup

def scrape_ecommerce():
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("[INFO] Connecting to target e-commerce platform...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    
    extracted_data = []
    
    for product in products:
        name = product.find("h3").find("a")["title"]
        
        price_str = product.find("p", class_="price_color").text.strip()
        price = price_str.replace("Â£", "£")
        
        rating_tag = product.find("p", class_="star-rating")
        rating = rating_tag["class"][1] if rating_tag else "Unrated"
        
        extracted_data.append({
            "Product Name": name,
            "Price": price,
            "Rating": rating
        })

    csv_filename = "products.csv"
    keys = ["Product Name", "Price", "Rating"]
    
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(extracted_data)
        
    print(f"[SUCCESS] Extracted {len(extracted_data)} products successfully!")
    print(f"[SAVED] Data exported to {csv_filename}")

if __name__ == "__main__":
    scrape_ecommerce()