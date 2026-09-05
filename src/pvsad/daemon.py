import time
import requests
import platform

API_URL = "http://127.0.0.1:8000/ingest"

def gather_local_telemetry() -> dict:
    return {
        "source": f"daemon-{platform.node()}",
        "timestamp": time.time(),
        "data": {
            "system": platform.system(),
            "release": platform.release(),
            "status": "local_hardware_check"
        }
    }

def run_daemon():
    print("[*] Initializing P-VSAD Vigilance Daemon...")
    payload = gather_local_telemetry()
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            receipt = response.json().get("receipt", {})
            print("[+] Success. Telemetry sealed.")
            print(f"    Hash Receipt: {receipt.get('payload_hash')}")
        else:
            print(f"[-] Backend rejected payload: {response.text}")
    except requests.exceptions.ConnectionError:
        print("[-] Connection failed. Verify the FastAPI backend is active on port 8000.")

if __name__ == "__main__":
    run_daemon()
