import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import atexit
import os

class CustomChrome(uc.Chrome):
    def __del__(self):
        pass  # Override the problematic destructor

class RedfinScraper:
    def __init__(self):
        self.driver = None
        atexit.register(self.cleanup)

    def cleanup(self):
        try:
            if self.driver:
                try:
                    self.driver.close()
                except:
                    pass
                try:
                    self.driver.quit()
                except:
                    pass
                
                # Force kill any remaining chrome processes
                if os.name == 'nt':  # Windows
                    os.system('taskkill /f /im chrome.exe >nul 2>&1')
                    os.system('taskkill /f /im chromedriver.exe >nul 2>&1')
        except:
            pass
        finally:
            self.driver = None

    def create_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = CustomChrome(options=options)
        return self.driver

    def get_estimate(self, url):
        try:
            if not self.driver:
                self.create_driver()
            
            self.driver.get(url)
            time.sleep(5)
            
            possible_selectors = [
                "//div[contains(@class, 'statsValue')]",
                "//div[contains(@class, 'home-value-wrapper')]//div[contains(@class, 'value')]",
                "//div[contains(@class, 'EstimateValues')]",
                "//span[contains(@data-rf-test-id, 'avmLdpPrice')]"
            ]
            
            estimate = None
            for selector in possible_selectors:
                try:
                    estimate_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    estimate = estimate_element.text
                    if estimate:
                        break
                except:
                    continue
            
            if estimate:
                print(f"Found Redfin Estimate: {estimate}")
                return estimate
            else:
                print("Could not find estimate on page")
                return None
                
        except Exception as e:
            print(f"Error getting estimate: {str(e)}")
            return None

    def search_and_get_estimate(self, address):
        try:
            self.create_driver()
            self.driver.get('https://www.redfin.com')
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "search-box-input"))
            )
            
            search_box.clear()
            search_box.send_keys(address)
            time.sleep(1)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            
            property_url = self.driver.current_url
            print(f"Found property URL: {property_url}")
            
            return self.get_estimate(property_url)
            
        except Exception as e:
            print(f"Error during search: {e}")
            return None
        finally:
            self.cleanup()

def main():
    try:
        scraper = RedfinScraper()
        address = input("Enter the property address to search: ")
        print(f"Searching for: {address}")
        
        estimate = scraper.search_and_get_estimate(address)
        if estimate:
            print(f"Final Redfin estimate: {estimate}")
        else:
            print("Failed to get property estimate")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    finally:
        if scraper:
            scraper.cleanup()

if __name__ == "__main__":
    main()