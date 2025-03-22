import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_meesho_price(product_url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.143 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Opening Meesho product page...")
        driver.get(product_url)
        time.sleep(5)  # Allow time for elements to load
        
        # Locate price element (Meesho's structure may change, so adjust if needed)
        price_element = driver.find_element(By.XPATH, "//h5[contains(text(), '₹')]" )
        price = price_element.text.strip()
        
        print(f"Product Price: {price}")
        return price
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    finally:
        driver.quit()

# Meesho product URL
product_url = "https://www.meesho.com/ice-blue-denim-wide-leg-denim-jeans/p/6fuaar"
print(get_meesho_price(product_url))