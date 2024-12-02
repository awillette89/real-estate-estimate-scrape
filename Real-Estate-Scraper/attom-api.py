import requests

def get_property_estimate(address, api_key):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/Resource/Package?{params}"
    params = {
        'address': address,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        estimate = data['attomavm']
        return estimate
    else:
        return f"Error: {response.status_code} - {response.text}"
    
if __name__ == "__main__":
    user_address = input("Enter the property address: ")
    api_key = "32b1e86b638620bf2404521e6e9e1b19e5f"
    estimate = get_property_estimate(user_address, api_key)
    print(f"The estimate value of the property at {user_address} is: {estimate}")