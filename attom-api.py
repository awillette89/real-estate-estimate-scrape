import urllib.parse
import http.client

def get_avm_snapshot(address1, address2, api_key):
    encoded_address1 = urllib.parse.quote(address1)
    encoded_address2 = urllib.parse.quote(address2)

    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")

    headers = {
        'accept': "application/json",
        'apikey': api_key
    }

    request_url = f"https://api.gateway.attomdata.com/propertyapi/v1.0.0/avm/snapshot?address1={encoded_address1}&address2={encoded_address2}"
    print(f"Request URL: {request_url}")

    conn.request("GET", request_url, headers=headers)
    
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        return data.decode("utf-8")
    else:
        return f"Error: {res.status} - {data.decode('utf-8')}"
    
if __name__ == "__main__":
    full_address = input("Enter the property address (e.g., 123 Main St, New York, NY): ")
    try:
        address_part, city_state = full_address.rsplit(',', 1)
        address1 = address_part.strip()
        address2 = city_state.strip()
    except ValueError:
        print("Error: Please enter the address in the correct format (123 Main St, New York, NY)")
        exit()

    api_key = ""
    avm_snapshot = get_avm_snapshot(address1, address2, api_key)
    print(f"The estimate value of the property at {full_address} is: {avm_snapshot}")