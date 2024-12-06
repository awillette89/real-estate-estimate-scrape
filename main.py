# Import necessary functions from attom_api
from attom_api import get_avm_snapshot, format_address
from redfin_estimate import RedfinScraper  # Correct import for RedfinScraper

def main():
    # Get user input for the address
    full_address = input("Please enter the address for home valuation (e.g., 123 Main St, New York, NY): ")

    # Format the address using the function from attom_api
    try:
        address1, address2 = format_address(full_address)
    except ValueError as ve:
        print(f"Error: {ve}")
        return  # Exit if the address format is incorrect

    api_key = ""  # Use your actual API key

    try:
        # Get home valuation from the ATTOM API
        avm_value = get_avm_snapshot(address1, address2, api_key)

        # Collect home valuations from Redfin
        redfin_scraper = RedfinScraper()  # Instantiate RedfinScraper
        value1_str = redfin_scraper.search_and_get_estimate(full_address)  # Get the estimate from Redfin
        
        # Clean up the Redfin estimate string
        value1 = float(value1_str.replace('$', '').replace(',', '')) if value1_str else 0.0

        # Calculate the average
        average_value = (avm_value + value1) / 2  # Average of ATTOM and Redfin values

        # Display the average to the user
        print(f"The average home valuation for '{full_address}' is: ${average_value:,.2f}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()