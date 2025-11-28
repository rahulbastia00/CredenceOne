from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from fastapi.responses import FileResponse
import os
import json

# Import the utility function
from app.utilities.sanction_utility import generate_sanction_letter_pdf

app = FastAPI(
    title="Agentic AI Sales Assistant Backend",
    description="Mock backend for KYC and Credit Bureau APIs.",
    version="1.0.0"
)

# --- CONFIGURING PATHS ---
# This gets the directory where THIS file (main.py) is located: .../backend/app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# This goes up one level to 'backend' and then into 'mock_data'
MOCK_DATA_DIR = os.path.join(BASE_DIR, "..", "mock_data")

def load_mock_json(filename: str):
    """Helper to read JSON files from the sibling mock_data directory."""
    file_path = os.path.join(MOCK_DATA_DIR, filename)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mock data file '{filename}' not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Error decoding '{filename}'. Check JSON format.")

# --- KYC ENDPOINTS (Used by Verification Agent) ---

@app.post("/api/verifyAadhaar")
async def verify_aadhaar(data: Dict[str, Any]):
    """
    Simulates Aadhaar verification by reading from mock_data/adhar-data.json
    """
    # Note: Using the exact spelling from your screenshot
    return load_mock_json("adhar-data.json")

@app.post("/api/verifyPan")
async def verify_pan(data: Dict[str, Any]):
    """
    Simulates PAN verification by reading from mock_data/pan-data.json
    """
    # Note: Using the exact spelling from your screenshot
    return load_mock_json("pan-data.json")

# --- CREDIT BUREAU ENDPOINT (Used by Underwriting Agent) ---

@app.post("/api/fetchCreditReport")
async def fetch_credit_report(data: Dict[str, Any]):
    """
    Simulates CIBIL Score fetch by reading from mock_data/cibil-data.json
    """
    # Note: Using the exact spelling from your screenshot
    return load_mock_json("cibil-data.json")


# --- Sanction Letter Test Endpoint ---
@app.post("/api/testSanctionLetter")
def test_sanction_letter_generation():
    """Test endpoint to generate a mock sanction letter."""
    try:
        customer_name = "Rahul Kumar Bastia"
        loan_amount = 450000.00
        tenure = 36
        rate = 11.0
        
        file_path = generate_sanction_letter_pdf(customer_name, loan_amount, tenure, rate)
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanction Letter Generation Failed: {e}")

# --- Health Check ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mock API is running with JSON integration"}