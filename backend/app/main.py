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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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


# -------------------- KYC ENDPOINTS --------------------

@app.post("/api/verifyAadhaar")
async def verify_aadhaar(data: Dict[str, Any]):
    """
    Verify Aadhaar by returning only the matched record from adhar-data.json.
    Expected input: { "aadhaarNumber": "594720183645" }
    """
    aadhaar_number = data.get("aadhaarNumber")

    if not aadhaar_number:
        raise HTTPException(status_code=400, detail="aadhaarNumber is required")

    json_data = load_mock_json("adhar-data.json")

    # Loop through JSON records
    for record in json_data.get("records", []):
        if record.get("aadhaarNumber") == aadhaar_number:
            return record  # <-- RETURNS ONLY THE MATCHED PERSON

    raise HTTPException(status_code=404, detail="No Aadhaar record found for the provided number")


@app.post("/api/verifyPan")
async def verify_pan(data: Dict[str, Any]):
    pan_number = data.get("panNumber")

    if not pan_number:
        raise HTTPException(status_code=400, detail="panNumber is required")

    json_data = load_mock_json("pan-data.json")

    # Check inside panVerificationRecords array
    for record in json_data.get("panVerificationRecords", []):
        if record.get("pan") == pan_number:
            return record

    raise HTTPException(status_code=404, detail="PAN record not found")



# -------------------- CREDIT REPORT CIBIL ENDPOINT --------------------

@app.post("/api/fetchCreditReport")
async def fetch_credit_report(data: Dict[str, Any]):
    """
    Fetch CIBIL report by PAN number from cibil-data.json.
    Expected input: { "panNumber": "AJPCE1298F" }
    """
    pan_number = data.get("panNumber")

    if not pan_number:
        raise HTTPException(status_code=400, detail="panNumber is required")

    json_data = load_mock_json("cibil-data.json")

    # Loop through cibilReports array
    for record in json_data.get("cibilReports", []):
        if record.get("panNumber") == pan_number:
            return record

    raise HTTPException(status_code=404, detail="No CIBIL report found for the provided PAN number")


# --- SANCTION LETTER TEST ---
@app.post("/api/testSanctionLetter")
def test_sanction_letter_generation():
    try:
        customer_name = "Rahul Kumar Bastia"
        loan_amount = 450000.00
        tenure = 36
        rate = 11.0

        file_path = generate_sanction_letter_pdf(customer_name, loan_amount, tenure, rate)
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanction Letter Generation Failed: {e}")


# --- HEALTH CHECK ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mock API is running with JSON integration"}
