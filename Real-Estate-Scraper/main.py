import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import time
import traceback
from contextlib import contextmanager
import re

@contextmanager
def create_driver(headless=False):
    driver = None
    try:
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = uc.Chrome(options=options, use_subprocess=True)
        yield driver
    except Exception as e:
        print(f"Error setting up driver: {e}")
        traceback.print_exc()
    finally:
        if driver:
            try:
                driver.execute_script("window.stop();")
            except Exception:
                pass
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")

def find_zestimate(driver):
    # Try to find Zestimate using various methods
    methods = [
        lambda: driver.find_element(By.CSS_SELECTOR, "[data-testid='zestimate']").text,
        lambda: driver.find_element(By.XPATH, "//span[contains(text(), 'Zestimate')]/following-sibling::span").text,
        lambda: re.search(r'"zestimate":(\d+)', driver.page_source).group(1),
        lambda: driver.execute_script("return (window.zestimate || window.Zestimate || {}).amount"),
    ]
    
    for method in methods:
        try:
            result = method()
            if result:
                return result
        except Exception:
            continue
    
    return "Not found"

def search_zillow(address, headless=False):
    with create_driver(headless) as driver:
        if not driver:
            return None, None

        try:
            wait = WebDriverWait(driver, 30)
            driver.get("https://www.zillow.com/")
            print("Loaded Zillow homepage")
            
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter an address, neighborhood, city, or ZIP code']")))
            search_box = wait.until(EC.visibility_of(search_box))
            
            search_box.clear()
            search_box.send_keys(address)
            search_box.submit()
            
            print("Submitted search")
            
            time.sleep(10)
            
            zestimate = find_zestimate(driver)
            print(f"Zestimate found: {zestimate}")

            return driver.current_url, zestimate

        except WebDriverException as e:
            print(f"WebDriver error: {e}")
            traceback.print_exc()
            return None, None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            return None, None

if __name__ == "__main__":
    try:
        address = input("Please input target address: ").strip()
        result_url, zestimate = search_zillow(address, headless=False)  # Set to True for headless mode
        if result_url:
            print(f"Search completed. Result URL: {result_url}")
            print(f"Zestimate: {zestimate}")
        else:
            print("Search failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Add a small delay before the script exits
        time.sleep(1)