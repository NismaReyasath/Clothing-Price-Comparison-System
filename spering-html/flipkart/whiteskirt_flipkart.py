from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_flipkart_price(product_url):
    # Automatically install correct ChromeDriver for Chrome 133
    service = Service(ChromeDriverManager(driver_version="133.0.6943.143").install())
    
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # ✅ Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Launch Chrome
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Opening Flipkart in headless mode...")
        driver.get(product_url)

        # Wait for price element to appear
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'_30jeq3 _16Jk6d')]")))

        # Extract price text
        price = price_element.text.strip() if price_element else "Price not found"

        # Get product name
        try:
            name_element = driver.find_element(By.XPATH, "//span[@class='B_NuCI']")
            product_name = name_element.text.strip()
        except:
            product_name = "Product Name Not Found"

        driver.quit()
        return f"Product: {product_name} | Price: {price}"

    except Exception as e:
        driver.quit()
        return f"Error: {str(e)}"

# Example Flipkart Product URL
product_url = "https://www.flipkart.com/utf-solid-women-pleated-white-skirt/p/itme9dcbe34cbb93?pid=SKIGJ2PNZZJCBBGH&lid=LSTSKIGJ2PNZZJCBBGH8TGVRG&marketplace=FLIPKART&q=white+pleated+skirt&store=clo%2Fvua%2Fiku%2Fw5t&srno=s_1_29&otracker=search&otracker1=search&fm=Search&iid=b8bf1c65-162c-481d-b5f5-e23327179c7f.SKIGJ2PNZZJCBBGH.SEARCH&ppt=sp&ppn=sp&ssid=rsqufsw1ps0000001741637315997&qH=80d36f0a5322b0f8"
print(get_flipkart_price(product_url))
