import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_all_product_links(driver, collection_url, max_products=25):
    """Scrapes all product links from the collection page."""
    product_links = []

    try:
        print("Opening collection page...")
        driver.get(collection_url)
        # Use WebDriverWait instead of sleep
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/product/')]"))
        )

        # Find all product links
        product_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")
        
        for product in product_elements:
            if len(product_links) >= max_products:
                break
            link = product.get_attribute("href")
            if link and link not in product_links:
                product_links.append(link)

    except Exception as e:
        print(f"Error while fetching product links: {e}")

    return product_links

def get_product_details(driver, product_url):
    """Extracts the product name, price, and rating from a product page."""
    product_info = {}

    try:
        print(f"Opening product page: {product_url}")
        driver.get(product_url)

        # Wait for product name to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1"))
        )

        # Get Product Name
        try:
            name_element = driver.find_element(By.XPATH, "//h1")
            product_name = name_element.text.strip()
        except Exception as e:
            print(f"Error fetching product name: {e}")
            product_name = f"Unknown Product ({e})"

        # Wait for product price to be present
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'price')]/span"))
            )
            product_price = price_element.text.strip()
        except Exception as e:
            print(f"Error fetching product price: {e}")
            product_price = f"Price Not Found ({e})"

        # Get Product Rating (if available)
        try:
            rating_element = driver.find_element(By.XPATH, "//div[contains(@class, 'jdgm-prev-badge__stars')]")
            product_rating = rating_element.get_attribute("aria-label")
        except Exception:
            product_rating = "Rating Not Available"

        product_info["name"] = product_name
        product_info["price"] = product_price
        product_info["rating"] = product_rating

    except Exception as e:
        print(f"Error fetching product details: {e}")

    return product_info

def scrape_product_details(product_urls, max_workers=5):
    """Scrapes product details in parallel using a shared WebDriver instance."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.89 Safari/537.36")

    # Create a shared WebDriver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_product_details = []

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(get_product_details, driver, url) for url in product_urls]
            for future in as_completed(futures):
                all_product_details.append(future.result())

    finally:
        driver.quit()

    return all_product_details

# Base Website URL
collection_url = "https://saashe.in/category/frock-style"

# Create a shared WebDriver instance for fetching product links
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.89 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Get all product links from the collection page (max 25 products)
product_links = get_all_product_links(driver, collection_url, max_products=25)
print(f"Total Products Found: {len(product_links)}")

driver.quit()

# Scrape product details for each product in parallel using a shared WebDriver instance
all_product_details = scrape_product_details(product_links, max_workers=10)

# Print final results
print("\n=== Scraped Product Details ===")
for index, product in enumerate(all_product_details, start=1):
    product_name = product.get('name', 'Unknown Product')
    product_price = product.get('price', 'Price Not Found')
    product_rating = product.get('rating', 'Rating Not Available')
    print(f"🔹 {product_name} {index} - {product_price} - ⭐ {product_rating}")