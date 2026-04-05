import requests
import time
import random
import json

API_URL = "http://localhost:8000/report"

def generate_disaster():
    disaster_types = ["Earthquake", "Flood"]
    locations = ["Zone-A", "Zone-B", "Zone-C", "Sector-7"]
    
    d_type = random.choice(disaster_types)
    location = random.choice(locations)
    
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
            response = requests.post(API_URL, json=payload)
            print(f"✅ Sent: {payload['type']} at {payload['location']} | Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"⏳ Generating data... (Backend offline): {json.dumps(payload)}")
            
        time.sleep(3)

if __name__ == "__main__":
    run_simulator()
