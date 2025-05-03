# utils/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_bill_pdf(guest_name, room_number, total_amount, output_path='bill.pdf'):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Hotel Automation System")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Guest Name: {guest_name}")
    c.drawString(100, 680, f"Room Number: {room_number}")
    c.drawString(100, 660, f"Total Amount: ₹{total_amount}")
    c.drawString(100, 620, "Thank you for staying with us!")

    c.save()
    return output_path
