import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_myntra_price_and_rating(product_url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Opening Myntra product page...")
        driver.get(product_url)
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to load

        # Locate price element
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'pdp-price')]")))
        price = price_element.text.strip()

        # Locate rating element
        rating_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'index-overallRating')]")))
        rating = rating_element.text.strip()

        print(f"Product Price: {price}")
        print(f"Product Rating: {rating}")
        return price, rating
    
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    
    finally:
        driver.quit()

# Myntra product URL
product_url = "https://www.myntra.com/tops/baesd/baesd-ribbed-tank-crop-top/24115434/buy"
get_myntra_price_and_rating(product_url)
