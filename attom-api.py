import urllib.parse
import http.client
import json

def get_avm_snapshot(address1, address2, api_key):
    encoded_address1 = urllib.parse.quote(address1 + " ")
    encoded_address2 = urllib.parse.quote(address2)

    conn = http.client.HTTPSConnection("api.gateway.attomdata.com")

    headers = {
        'accept': "application/json",
        'apikey': api_key
    }

    request_url = f"https://api.gateway.attomdata.com/propertyapi/v1.0.0/attomavm/detail?address1={encoded_address1}&address2={encoded_address2}"

    conn.request("GET", request_url, headers=headers)
    
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        response_data = json.loads(data.decode("utf-8"))
        try:
            value = response_data['property'][0]['avm']['amount']['value']
            return value
        except (KeyError, IndexError):
            return "Value not found in response."
    else:
        return f"Error: {res.status} - {data.decode('utf-8')}"

def format_address(full_address):
    if ',' not in full_address:
        raise ValueError("Address must include a comma separating the street and city/state.")
    
    address_part, city_state = full_address.split(',', 1)
    address1 = address_part.strip()
    city_state = city_state.strip()

    if ' ' not in city_state:
        raise ValueError("City and state must be provided in the format 'City, State'.")

    parts = city_state.rsplit(' ', 1)
    if len(parts) != 2:
        raise ValueError("City and state must be provided in the format 'City, State'.")

    city = parts[0].strip()
    state = parts[1].strip().upper()

    address2 = f"{city}, {state}"

    return address1, address2

if __name__ == "__main__":
    full_address = input("Enter the property address (e.g., 123 Main St, New York, NY): ")
    try:
        address1, address2 = format_address(full_address)
    except ValueError as ve:
        print(f"Error: {ve}")
        exit()

    api_key = ""
    avm_value = get_avm_snapshot(address1, address2, api_key)
    
    if isinstance(avm_value, int):  
        print(f"The estimated value of the property at {full_address} is: ${avm_value}")
    else:
        print(avm_value)