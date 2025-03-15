import base64
import json
import os
import requests
from datetime import datetime, timedelta

# Function to generate an OAuth2 access token
def get_access_token(CLIENT_ID, CLIENT_SECRET):
    TOKEN_FILE = "nameOfTokenToStoreUrEbayToken.json"
    # Check if the token already exists and is valid
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            token_data = json.load(file)
            expiration_time = datetime.fromisoformat(token_data["expires_at"])
            if expiration_time > datetime.now():
                return token_data["access_token"]

    # If the token is expired or doesn't exist, generate a new one
    auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_auth = base64.b64encode(auth.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}",
    }

    API_SCOPE = "https://api.ebay.com/oauth/api_scope"           # scope aka what it how much of ebay resources it has access
    OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"  # send post request to this link to get token

    data = {
        "grant_type": "client_credentials",
        "scope": API_SCOPE,
    }

    response = requests.post(OAUTH_URL, headers=headers, data=data)
    if response.status_code == 200:
        token_response = response.json()
        access_token = token_response["access_token"]
        expires_in = token_response["expires_in"]

        # Store the token and expiration time locally
        token_data = {
            "access_token": access_token,
            "expires_at": (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
        }
        with open("ebay_token.json", "w") as file:
            json.dump(token_data, file)

        return access_token
    else:
        raise Exception(f"Error generating token: {response.status_code} {response.text}")

# Function to make an authenticated eBay API request
def make_ebay_api_request(access_token, query=str, ammount=int):
    access_token = access_token

    # Define the eBay Browse API endpoint
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    params = {
        "q": query,
        "filter": "buyingOptions:{AUCTION}",
        "limit": ammount,
    }

    response = requests.get(url, headers=headers, params=params)
    ebay_search_results = []

    if response.status_code == 200:
        results = response.json().get("itemSummaries", [])
        if not results:
            return "No auctions found"

        # Format and display the results
        for item in results:
            title = item.get("title", "N/A")
            price =  item.get("currentBidPrice", {}).get("value")
            currency = item.get("currentBidPrice", {}).get("currency", "N/A")
            end_date = item.get("itemEndDate", "N/A")
            
            # Parse and format the auction end time
            if end_date != "N/A":
                end_time = datetime.fromisoformat(end_date[:-1]).strftime("%Y-%m-%d %H:%M:%S")
            else:
                end_time = "N/A"

            ebay_search_results.append([title, price, currency, end_date, item.get('itemWebUrl', 'N/A')])

        return ebay_search_results
    else:
        print(f"Error: {response.status_code} - {response.text}")
