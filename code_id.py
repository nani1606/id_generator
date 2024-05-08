# import csv
# import os
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from PIL import Image

# def create_id_pdf(template_path, csv_file_path, photo_directory, output_path):
#     try:
#         employee_data = []

#         with open(csv_file_path, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 employee_data.append(row)

#         pdf_doc = canvas.Canvas(output_path, pagesize=letter)

#         for employee in employee_data:
#             template = Image.open(template_path)
#             pdf_doc.drawImage(template_path, 0, 0, width=template.width, height=template.height)

#             photo_path = os.path.join(photo_directory, employee['photo_path'])
#             photo = Image.open(photo_path)
#             pdf_doc.drawImage(photo_path, 175, 19, width=122, height=120)  # Adjust coordinates and dimensions as needed

#             name = employee['name']
#             title = employee['position']

#             pdf_doc.setFont("Helvetica", 12)
#             pdf_doc.drawString(110, 180, name)  # Adjust coordinates as needed
#             pdf_doc.drawString(90, 200, title)  # Adjust coordinates as needed

#             pdf_doc.showPage()

#         pdf_doc.save()
#         print('PDF created successfully!')
#     except Exception as error:
#         print('Error:', error)

# # Usage example
# template_path = './public/id_template.png'
# csv_file_path = './employees.csv'
# photo_directory = './images'
# output_path = 'output_id_cards.pdf'

# create_id_pdf(template_path, csv_file_path, photo_directory, output_path)


import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont

def create_id_pdf(template_path, csv_file_path, photo_directory, output_path):
    try:
        # Load template image
        template = Image.open(template_path)

        # Load CSV data
        employee_data = []
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                employee_data.append(row)

        # Create PDF document
        c = canvas.Canvas(output_path, pagesize=letter)

        for employee in employee_data:
            # Draw template on page
            c.drawImage(template_path, 0, 0, width=template.width, height=template.height)

            # Load employee photo
            photo_path = os.path.join(photo_directory, employee['photo_path'])
            photo = Image.open(photo_path)

            # Draw photo on page
            c.drawImage(photo_path, 175, 65, width=122, height=120)

            # Draw employee name
            c.setFont("Helvetica", 18)
            c.drawString(110, 10, employee['name'])

            # Draw employee position
            c.setFont("Helvetica", 18)
            c.drawString(90, 25, employee['position'])

            # Add new page for the next employee
            c.showPage()

        # Save PDF document
        c.save()
        print('PDF created successfully!')
    except Exception as e:
        print('Error:', e)

# Usage example
template_path = './public/id_template.png'
csv_file_path = './employees.csv'
photo_directory = './images'
output_path = 'output_id_cards.pdf'

create_id_pdf(template_path, csv_file_path, photo_directory, output_path)
