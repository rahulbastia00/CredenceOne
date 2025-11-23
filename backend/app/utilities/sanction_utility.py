from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

def generate_sanction_letter_pdf(customer_name: str, loan_amount: float, tenure: int, rate: float) -> str:
    """
    Generates a mock Sanction Letter PDF based on approved loan details.

    Args:
        customer_name: The name of the customer.
        loan_amount: The sanctioned loan amount.
        tenure: The loan tenure in months.
        rate: The annual interest rate.

    Returns:
        The file path of the generated PDF.
    """
    
    # Ensure a directory exists for generated files (optional, but good practice)
    output_dir = "generated_documents"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    safe_name = customer_name.replace(' ', '_').lower()
    file_name = os.path.join(output_dir, f"sanction_letter_{safe_name}.pdf")

    c = canvas.Canvas(file_name, pagesize=letter)
    
    # Set up basic font
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, 10.5 * inch, "TATA CAPITAL (MOCK) - LOAN SANCTION LETTER")
    c.setFont("Helvetica", 10)
    c.drawString(inch, 10.25 * inch, "Reference: Mock-LSR-987654321")
    
    # Draw content
    c.setFont("Helvetica", 12)
    y_pos = 9.5 * inch
    c.drawString(inch, y_pos, f"Date: {os.fspath('2025-11-23')}")
    y_pos -= 0.5 * inch
    c.drawString(inch, y_pos, f"Dear {customer_name},")
    y_pos -= 0.25 * inch
    c.drawString(inch, y_pos, "We are pleased to inform you that your application for a Personal Loan has been approved.")
    
    # Loan Details Table
    y_pos -= 0.5 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1.5 * inch, y_pos, "Loan Details:")
    
    c.setFont("Helvetica", 12)
    y_pos -= 0.25 * inch
    
    details = [
        ("Sanctioned Amount:", f"₹{loan_amount:,.2f}"),
        ("Tenure:", f"{tenure} months"),
        ("Interest Rate (Annual):", f"{rate}%"),
    ]
    
    x_col1 = 1.5 * inch
    x_col2 = 4.5 * inch
    
    for label, value in details:
        c.drawString(x_col1, y_pos, label)
        c.drawString(x_col2, y_pos, value)
        y_pos -= 0.25 * inch
        
    # Footer Note
    y_pos -= 0.5 * inch
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(inch, 1 * inch, "NOTE: This document is a mock output for demonstrating the system architecture.")
    
    c.save()

    # Return the file name for confirmation
    return file_name

# Example test call (will not run when imported by FastAPI, but useful for quick testing)
if __name__ == '__main__':
    mock_file = generate_sanction_letter_pdf("Rahul Kumar Bastia", 500000.00, 48, 10.5)
    print(f"Mock Sanction Letter generated successfully at: {mock_file}")