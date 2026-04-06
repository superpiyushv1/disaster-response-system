from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DisasterData(BaseModel):
    type: str
    location: str
    value: float
    timestamp: str

@app.get("/")
def read_root():
    return {"status": "The Disaster Backend is Alive!"}

@app.post("/report")
def receive_report(data: DisasterData):
    
    severity_level = "NORMAL"
    
    if data.type == "Earthquake" and data.value >= 6.0:
        severity_level = "HIGH_ALERT"
    elif data.type == "Flood" and data.value >= 8.0:
        severity_level = "HIGH_ALERT"

    
    print(f"🚨 Received: {data.type} in {data.location} | Severity: {severity_level}")

   
    return {"status": "success", "severity": severity_level}
