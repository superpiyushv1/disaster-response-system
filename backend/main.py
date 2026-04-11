from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import httpx
from fastapi.middleware.cors import CORSMiddleware # New Import

# Load the secret variables from the .env file
load_dotenv(dotenv_path="backend/.env")

app = FastAPI()

# --- STEP 1: ENABLE CORS ---
# This allows your index.html file to talk to your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# The Public Channel messenger function
async def send_telegram_alert(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram keys missing. Cannot send alert.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(url, json=payload)

        if response.status_code == 200:
            print(f"📱 Telegram Alert Broadcasted to {TELEGRAM_CHAT_ID} Successfully!")
        else:
            print(f"❌ Telegram Error: {response.status_code} - {response.text}")

# --- STEP 2: NEW GET ROUTE FOR THE MAP ---
@app.get("/get-disasters")
async def get_disasters():
    # Fetch the latest 20 disasters from MongoDB
    cursor = collection.find().sort("timestamp", -1).limit(20)
    disasters = await cursor.to_list(length=20)
    for d in disasters:
        d["_id"] = str(d["_id"])  # Convert MongoDB ID to string for JSON
    return disasters

@app.get("/")
def read_root():
    return {"status": "The Disaster Backend is Alive!", "db_connected": "True" if MONGO_URI else "False"}

@app.post("/report")
async def receive_report(data: DisasterData):
    severity_level = "NORMAL"
    
    if data.type == "Earthquake" and data.value >= 6.0:
        severity_level = "HIGH_ALERT"
    elif data.type == "Flood" and data.value >= 8.0:
        severity_level = "HIGH_ALERT"

    report_dict = data.model_dump() 
    report_dict["severity"] = severity_level
    await collection.insert_one(report_dict)

    print(f"🚨 Saved to DB: {data.type} in {data.location} | Severity: {severity_level}")

    if severity_level == "HIGH_ALERT":
        alert_text = f"⚠️ CRITICAL ALERT: {data.type} detected in {data.location}! Magnitude/Value: {data.value}"
        await send_telegram_alert(alert_text)

    return {"status": "success", "severity": severity_level, "message": "Saved to cloud database"}
