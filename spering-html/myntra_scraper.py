import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_myntra_price_and_rating(product_name, product_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(product_url)
        wait = WebDriverWait(driver, 10)

        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'pdp-price')]")))
        price = price_element.text.strip()

        rating_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'index-overallRating')]")))
        rating = rating_element.text.strip()

        return {"name": product_name, "price": price, "rating": rating, "url": product_url}

    except Exception as e:
        print(f"Error scraping {product_name}: {e}")
        return {"name": product_name, "price": "N/A", "rating": "N/A", "url": product_url}

    finally:
        driver.quit()

# List of Myntra products
myntra_products = [
    {"name": "Ribbed Tank Crop Top", "url": "https://www.myntra.com/tops/baesd/baesd-ribbed-tank-crop-top/24115434/buy"},
    {"name": "Wide Leg Jeans", "url": "https://www.myntra.com/jeans/aadvi+fashion/aadvi-fashion-women-original-high-rise-stretchable-wide-leg-jeans/32481893/buy"},
    {"name": "Maxi Skirt", "url": "https://www.myntra.com/skirts/neudis/neudis-pure-cotton-flared-maxi-skirts/30198724/buy"},
    {"name": "Kurta Set", "url": "https://www.myntra.com/kurta-sets/krati+creations/krati-creations-floral-printed-band-collar-a-line-kurta-with-palazzos/30409643/buy"}
]

# Scrape and save data
myntra_data = [get_myntra_price_and_rating(p["name"], p["url"]) for p in myntra_products]

# Save data to JSON file
with open("data.json", "w") as f:
    json.dump(myntra_data, f, indent=4)

print("Data saved to data.json!")
