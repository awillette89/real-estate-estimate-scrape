import asyncio
from playwright.async_api import async_playwright
import re
import urllib.parse

async def get_zillow_zestimate(address, max_retries=3):
    url = f"https://www.zillow.com/homes/{urllib.parse.quote(address)}_rb/"
    
    async with async_playwright() as p:
        for attempt in range(max_retries):
            browser = await p.firefox.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
            )
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                await asyncio.sleep(10)  # Wait for 10 seconds after initial load
                
                # Scroll the page
                for _ in range(5):
                    await page.evaluate("window.scrollBy(0, 300)")
                    await asyncio.sleep(1)
                
                # Extract all text content from the page
                content = await page.evaluate("() => document.body.innerText")
                
                # Extract Zestimate
                zestimate_match = re.search(r'Zestimate.*?\$([\d,]+)', content, re.IGNORECASE | re.DOTALL)
                if zestimate_match:
                    return f"${zestimate_match.group(1)}"
                
                print(f"Attempt {attempt + 1}: Failed to extract Zestimate.")
                if attempt == max_retries - 1:
                    return None

            except Exception as e:
                print(f"Attempt {attempt + 1}: An error occurred: {e}")
                if attempt == max_retries - 1:
                    return None
            
            finally:
                await context.close()
                await browser.close()
                await asyncio.sleep(5)  # Wait between retries

async def main():
    while True:
        address = input("Enter an address (or 'quit' to exit): ")
        if address.lower() == 'quit':
            break
        
        print("Fetching Zestimate from Zillow...")
        zestimate = await get_zillow_zestimate(address)
        
        if zestimate:
            print(f"\nZestimate for {address}: {zestimate}")
        else:
            print("Failed to retrieve Zestimate.")
        
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())