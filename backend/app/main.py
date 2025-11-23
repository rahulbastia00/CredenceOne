from fastapi import FastAPI, HTTPException
from typing import Dict, Any
# Import the utility function
from app.utilities.sanction_utility import generate_sanction_letter_pdf
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Agentic AI Sales Assistant Backend",
    description="Mock backend for KYC and Credit Bureau APIs, and Sanction Utility test.",
    version="1.0.0"
)

# --- Sanction Letter Test Endpoint (Temporary for Utility Check) ---
@app.post("/api/testSanctionLetter")
def test_sanction_letter_generation():
    """
    Test endpoint to generate a mock sanction letter and return it.
    Uses hardcoded data for immediate testing.
    """
    try:
        # Hardcoded data simulating a successful loan approval
        customer_name = "Rahul Kumar Bastia"
        loan_amount = 450000.00
        tenure = 36
        rate = 11.0
        
        file_path = generate_sanction_letter_pdf(customer_name, loan_amount, tenure, rate)
        
        # Return the file as a response for easy testing in the browser/API tool
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanction Letter Generation Failed: {e}")

# --- Health Check Endpoint ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mock API is running"}