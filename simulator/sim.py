import requests
import time
import random
import json

# 🚨 FIXED: Added /report to the end of the URL
API_URL = "https://disaster-backend-api-7bvx.onrender.com/report" 

# The authentic Indian locations database
LOCATIONS = [
    # --- NCR Hotspots ---
    "Janakpuri, New Delhi",
    "Connaught Place, New Delhi",
    "Hauz Khas, New Delhi",
    "Vasant Kunj, New Delhi",
    "Karol Bagh, New Delhi",
    "Cyber City, Gurugram",
    "Sector 56, Gurugram",
    "Noida Sector 18, UP",
    "Indirapuram, Ghaziabad",
    "Sector 15, Faridabad",
    
    # --- Major Hubs Across India ---
    "Bandra West, Mumbai",
    "Andheri East, Mumbai",
    "Whitefield, Bengaluru",
    "Koramangala, Bengaluru",
    "Salt Lake, Kolkata",
    "Park Street, Kolkata",
    "Jubilee Hills, Hyderabad",
    "HITEC City, Hyderabad",
    "MG Road, Pune",
    "Koregaon Park, Pune",
    "T-Nagar, Chennai",
    "Anna Nagar, Chennai",
    "Ambawadi, Ahmedabad",
    "Hazratganj, Lucknow",
    "Civil Lines, Jaipur"
] # Fixed missing bracket

def generate_disaster():
    disaster_types = ["Earthquake", "Flood"]
    
    d_type = random.choice(disaster_types)
    location = random.choice(LOCATIONS)
    
    if d_type == "Earthquake":
        value = round(random.uniform(3.0, 9.5), 1)
    else:
        value = round(random.uniform(2.0, 15.0), 1)

    return {
        "type": d_type,
        "location": location,
        "value": value,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def run_simulator():
    print("🌍 Data Simulator Started. Press Ctrl+C to stop.")
    while True:
        payload = generate_disaster()
        try:
            # Added a timeout to help with cloud cold-starts
            response = requests.post(API_URL, json=payload, timeout=10)
            print(f"✅ Sent: {payload['type']} ({payload['value']}) at {payload['location']} | Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⏳ Connection Error: {e}")

        time.sleep(3)

if __name__ == "__main__":
    run_simulator()
