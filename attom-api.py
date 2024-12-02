import urllib.parse
import http.client

def get_property_estimate(address, api_key):
    encoded_address1 = urllib.parse.quote(address1)
    encoded_address2 = urllib.parse.quote(address2)
    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")

    headers = {
        'accept': "application/json",
        'apikey': api_key
    }

    request_url = f"/avm/snapshot?address1={encoded_address1}&address2={encoded_address2}"
    print(f"Request URL: {request_url}")

    conn.request("GET", request_url, headers=headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        return data.decode("utf-8")
    else:
        return f"Error: {res.status} - {data.decode('utf-8')}"
    
if __name__ == "__main__":
    user_address = input("Enter the property address (e.g., 123 Main St, New York, NY): ")
    try:
        address1, address2 = user_address.rsplit(',', 1)
        address1 = address1.strip()
        address2 = address2.strip()
    except ValueError:
        print("Error: Please enter the address in the correct format (123 Main St, New York, NY)")
        exit()

    api_key = "16f91d5a2123ffe12ca98f248bce059a"
    estimate = get_property_estimate(user_address, api_key)
    print(f"The estimate value of the property at {user_address} is: {estimate}")