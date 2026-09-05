import os
import hashlib
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

load_dotenv()

app = FastAPI(title="P-VSAD Verification Engine", version="3.2.0")

class TelemetryPayload(BaseModel):
    source: str
    timestamp: float
    data: dict

def load_private_key():
    pem_string = os.environ.get("PVSAD_PRIVATE_KEY")
    if not pem_string:
        raise ValueError("PVSAD_PRIVATE_KEY not found in environment. Run keygen.py first.")
    pem_string = pem_string.strip("'")
    return serialization.load_pem_private_key(pem_string.encode('utf-8'), password=None)

def sign_hash(hash_hex: str) -> str:
    private_key = load_private_key()
    signature = private_key.sign(hash_hex.encode('utf-8'))
    return signature.hex()

def canonicalize_and_hash(payload: dict) -> str:
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    hash_object = hashlib.sha3_512(canonical_json.encode('utf-8'))
    return hash_object.hexdigest()

@app.post("/ingest")
async def ingest_telemetry(payload: TelemetryPayload):
    try:
        raw_data = payload.model_dump() 
        computed_hash = canonicalize_and_hash(raw_data)
        signature = sign_hash(computed_hash)
        
        receipt = {
            "status": "sealed_and_signed",
            "algorithm": "SHA3-512 + Ed25519",
            "payload_hash": computed_hash,
            "cryptographic_signature": signature,
            "timestamp": payload.timestamp,
            "source": payload.source
        }
        return {"message": "Telemetry cryptographically sealed.", "receipt": receipt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
