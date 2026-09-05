import hashlib
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="P-VSAD Verification Engine", version="3.1.0")

class TelemetryPayload(BaseModel):
    source: str
    timestamp: float
    data: dict

def canonicalize_and_hash(payload: dict) -> str:
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    hash_object = hashlib.sha3_512(canonical_json.encode('utf-8'))
    return hash_object.hexdigest()

@app.post("/ingest")
async def ingest_telemetry(payload: TelemetryPayload):
    try:
        raw_data = payload.model_dump() 
        computed_hash = canonicalize_and_hash(raw_data)
        
        receipt = {
            "status": "sealed",
            "algorithm": "SHA3-512",
            "payload_hash": computed_hash,
            "timestamp": payload.timestamp,
            "source": payload.source
        }
        return {"message": "Telemetry sealed.", "receipt": receipt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
