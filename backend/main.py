from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import httpx

# Load the secret variables from the .env file
load_dotenv(dotenv_path="backend/.env")

app = FastAPI()

# Database & Telegram Variables
MONGO_URI = os.getenv("MONGO_URI")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = AsyncIOMotorClient(MONGO_URI)
db = client.disaster_database        
collection = db.reports              

class DisasterData(BaseModel):
    type: str
    location: str
    value: float
    timestamp: str

# The upgraded messenger function
async def send_telegram_alert(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram keys missing. Cannot send alert.")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(url, json=payload)
        
        # Check if Telegram accepted the message
        if response.status_code == 200:
            print("📱 Telegram Alert Delivered Successfully!")
        else:
            print(f"❌ Telegram Error: {response.status_code} - {response.text}")

@app.get("/")
def read_root():
    return {"status": "The Disaster Backend is Alive!", "db_connected": MONGO_URI is not None}

@app.post("/report")
async def receive_report(data: DisasterData):
    severity_level = "NORMAL"
    
    if data.type == "Earthquake" and data.value >= 6.0:
        severity_level = "HIGH_ALERT"
    elif data.type == "Flood" and data.value >= 8.0:
        severity_level = "HIGH_ALERT"

    # Package the data and save to MongoDB
    report_dict = data.model_dump() 
    report_dict["severity"] = severity_level
    await collection.insert_one(report_dict)

    print(f"🚨 Saved to DB: {data.type} in {data.location} | Severity: {severity_level}")

    # Trigger the alarm if things are critical
    if severity_level == "HIGH_ALERT":
        alert_text = f"⚠️ CRITICAL ALERT: {data.type} detected in {data.location}! Level: {data.value}"
        await send_telegram_alert(alert_text)

    return {"status": "success", "severity": severity_level, "message": "Saved to database"}
