import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_meesho_price_and_rating(product_name, product_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"Fetching data for {product_name}...")
        driver.get(product_url)
        time.sleep(5)

        price_element = driver.find_element(By.XPATH, "//h5[contains(text(), '₹')]")
        price = price_element.text.strip()

        return {"name": product_name, "price": price, "rating": "N/A", "url": product_url}

    except Exception as e:
        print(f"Error scraping {product_name}: {e}")
        return {"name": product_name, "price": "N/A", "rating": "N/A", "url": product_url}

    finally:
        driver.quit()

# List of Meesho products
meesho_products = [
    {"name": "Tusi Tank Top Combo", "url": "https://www.meesho.com/tusi-tank-top-combo-black-white-01/p/8cf9tj"},
    {"name": "Ice Blue Denim Wide Leg Jeans", "url": "https://www.meesho.com/ice-blue-denim-wide-leg-denim-jeans/p/6fuaar"},
    {"name": "Trendy Letest Woman Skirt", "url": "https://www.meesho.com/kk-trendy-letest-woman-skirt/p/6mzsoc"},
    {"name": "Magic Cotton Kurta Set", "url": "https://www.meesho.com/magic-cotton-kurta-set/p/7stacy"}
]

# Scrape and save data
meesho_data = [get_meesho_price_and_rating(p["name"], p["url"]) for p in meesho_products]

# Save data to JSON file
with open("meesho_data.json", "w") as f:
    json.dump(meesho_data, f, indent=4)

print("Meesho data saved to meesho_data.json!")
