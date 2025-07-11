import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
from PyPDF2 import PdfMerger
import os

# Step 1: Load Order Data
def load_orders(filename):
    orders = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Quantity'] = int(row['Quantity'])
            row['Unit Price'] = float(row['Unit Price'])
            row['Total Amount'] = row['Quantity'] * row['Unit Price']
            orders.append(row)
    return orders

# Step 2: Generate PDF Invoices
def generate_pdf_invoice(order, output_directory="invoices_folder"):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    order_id = order['Order ID']
    customer_name = order['Customer Name']
    product_name = order['Product Name']
    quantity = order['Quantity']
    unit_price = order['Unit Price']
    total_amount = order['Total Amount']
    purchase_date = datetime.now().strftime("%Y-%m-%d")

    # Create PDF
    pdf_filename = f"{output_directory}/Invoice_{order_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    
    # Add content to PDF
    c.setFont("Helvetica", 12)
    
    # Invoice Header
    c.drawString(20*mm, 270*mm, f"Invoice Number: {order_id}")
    c.drawString(20*mm, 260*mm, f"Date of Purchase: {purchase_date}")
    
    # Customer Information
    c.drawString(20*mm, 240*mm, f"Customer Name: {customer_name}")
    
    # Order Details
    c.drawString(20*mm, 220*mm, f"Product Name: {product_name}")
    c.drawString(20*mm, 210*mm, f"Quantity: {quantity}")
    c.drawString(20*mm, 200*mm, f"Unit Price: ${unit_price:.2f}")
    c.drawString(20*mm, 190*mm, f"Total Amount: ${total_amount:.2f}")

    # Save PDF
    c.showPage()
    c.save()

    return pdf_filename

# Step 3: Merge PDFs into a Single File
def merge_pdfs(pdf_files, output_filename="Merged_Invoices.pdf"):
    merger = PdfMerger()
    
    for pdf in pdf_files:
        merger.append(pdf)

    # Write to final output PDF file
    merger.write(output_filename)
    merger.close()

# Main function to run the process
def create_invoices(csv_filename):
    orders = load_orders(csv_filename)
    pdf_files = []
    
    # Generate individual PDFs
    for order in orders:
        pdf_file = generate_pdf_invoice(order)
        pdf_files.append(pdf_file)
    
    # Merge all PDFs
    merge_pdfs(pdf_files)

    print(f"All invoices merged into 'Merged_Invoices.pdf'.")

# Usage
csv_filename = "orders.csv"
create_invoices(csv_filename)