from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# 1. Load the secret variables from the .env file
load_dotenv(dotenv_path="backend/.env")

app = FastAPI()

# 2. Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.disaster_database        # Creates a database called 'disaster_database'
collection = db.reports              # Creates a table/collection called 'reports'

class DisasterData(BaseModel):
    type: str
    location: str
    value: float
    timestamp: str

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

    # Package the incoming data into a dictionary
    report_dict = data.model_dump() # Note: .dict() is deprecated in newer Pydantic, model_dump() is better!
    report_dict["severity"] = severity_level

    # 3. Insert it permanently into MongoDB Cloud
    await collection.insert_one(report_dict)

    print(f"🚨 Saved to DB: {data.type} in {data.location} | Severity: {severity_level}")

    return {"status": "success", "severity": severity_level, "message": "Saved to database"}
