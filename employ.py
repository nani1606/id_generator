import csv
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def generate_id_cards(csv_file, image_dir, output_pdf):
    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        employee_data = list(reader)

    # Create PDF document
    card_width, card_height = (225, 350)  # Adjust page size to match ID card size
    c = canvas.Canvas(output_pdf, pagesize=(card_width, card_height))
    for i, employee in enumerate(employee_data):
        # Load image
        image_extensions = ['.jpg', '.jpeg', '.png']  # Supported image extensions
        img_path = None
        for ext in image_extensions:
            image_path = os.path.join(image_dir, employee['name'] + ext)
            if os.path.exists(image_path):
                img_path = image_path
                break
        if img_path is None:
            print(f"Image not found for employee {employee['name']}")
            continue

        img = Image.open(img_path)
        img_width, img_height = img.size

        # Calculate scaling factors to fit image within card size
        scale_width = card_width * 0.8 / img_width
        scale_height = card_height * 0.4 / img_height
        scale_factor = min(scale_width, scale_height)

        # Resize image
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        img = img.resize((new_width, new_height))

        # Save resized image to a temporary file
        temp_dir = tempfile.mkdtemp()
        temp_img_path = os.path.join(temp_dir, f"{employee['name']}.png")
        img.save(temp_img_path)

        # Add employee data to ID card
        c.drawString(20, 300, f"Name: {employee['name']}")
        c.drawString(20, 280, f"Title: {employee['title']}")
        # Add more fields as needed

        # Add image to ID card
        c.drawImage(temp_img_path, 20, 100, width=new_width, height=new_height)

        # Add page break for next ID card
        if i < len(employee_data) - 1:
            c.showPage()

    # Save PDF document
    c.save()

# Paths
csv_file = "employee_data.csv"
image_dir = "images"
output_pdf = "id_cards.pdf"

# Generate ID cards
generate_id_cards(csv_file, image_dir, output_pdf)

#edits