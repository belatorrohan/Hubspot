import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# HubSpot API Token
HUBSPOT_API_TOKEN = 'pat-na1-d769cb77-9c88-4067-b259-c6b8251ad43b'

# Function to fetch referees
def get_referrals(referral_code):
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # HubSpot Search Query
    payload = {
        "filterGroups": [
            {
                "filters": [
                    {"propertyName": "referral_code", "operator": "EQ", "value": referral_code}
                ]
            }
        ],
        "properties": ["firstname", "lastname", "lifecyclestage"],  # Add more properties if needed
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Error fetching referrals:", response.status_code, response.text)
        return []

# API Endpoint to fetch referrals
@app.route('/get-referrals', methods=['GET'])
def get_referrals_endpoint():
    referral_code = request.args.get('referral_code')
    if not referral_code:
        return jsonify({"error": "Referral code is required"}), 400

    referrals = get_referrals(referral_code)
    return jsonify(referrals)

if __name__ == "__main__":
    app.run(debug=True)
