import pymongo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import Tk, Button, filedialog
from PIL import Image
from io import BytesIO
from reportlab.lib.utils import ImageReader

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["employee_database"]
details_collection = db["employee_details"]
image_collection = db["employee_images"]

# Function to handle image selection and upload
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Store image in MongoDB
        upload_image(file_path)

# Function to upload image to MongoDB
def upload_image(file_path):
    with open(file_path, "rb") as f:
        image_data = f.read()

    # Prompt user for details
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    position = input("Enter your position: ")

    # Store data in MongoDB
    employee_data = {
        "first_name": first_name,
        "last_name": last_name,
        "position": position,
        "image": image_data
    }
    details_collection.insert_one(employee_data)

    # Confirm insertion
    print("Employee details and image uploaded successfully.")

# Function to generate ID cards as PDF
def generate_id_cards():
    # Create PDF document
    output_pdf = "id_cards.pdf"
    c = canvas.Canvas(output_pdf, pagesize=letter)

    try:
        # Retrieve employee details and images from MongoDB
        for employee in details_collection.find():
            first_name = employee["first_name"]
            last_name = employee["last_name"]
            position = employee["position"]
            image_data = employee["image"]

            # Convert image data to PIL Image
            img = Image.open(BytesIO(image_data))

            # Define ID card layout
            card_width, card_height = (600, 400)  # Adjusted template size
            c.setFillColorRGB(1, 1, 1)  # White background
            c.rect(0, 0, card_width, card_height, fill=True)  # Add background rectangle

            # Add header background
            c.setFillColorRGB(0.2, 0.6, 0.4)  # Greenish color
            c.rect(50, 350, 500, 40, fill=True)

            # Add header text
            c.setFillColorRGB(1, 1, 1)  # White color
            c.setFont("Helvetica-Bold", 24)
            c.drawString(180, 362, "Employee ID Card")  # Adjusted position

            # Add image
            img_width, img_height = (100, 100)  # Adjusted image size
            img_x = (card_width - img_width - 10) / 2  # Center image horizontally
            img_y = 200  # Position image vertically
            c.drawImage(ImageReader(img), img_x, img_y, width=img_width, height=img_height)

            # Add name text
            c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(0, 0, 0)  # Black color
            c.drawString(75, 120, "Name:")
            c.setFont("Helvetica", 14)
            c.drawString(130, 120, f"{first_name} {last_name}")

            # Add position text
            c.setFont("Helvetica-Bold", 16)
            c.drawString(75, 80, "Position:")
            c.setFont("Helvetica", 14)
            c.drawString(150, 80, position)

            # Add footer
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.2, 0.2, 0.2)  # Dark gray color
            c.drawString(50, 30, "Generated by YourCompany")

            # Save PDF document
            c.showPage()

        # Save PDF document
        c.save()
        print("ID cards generated successfully.")
    except Exception as e:
        print("An error occurred while generating ID cards:", e)

# Create GUI window
root = Tk()
root.title("Employee Details")
root.geometry("300x200")

# Create 'Add Image' button
add_image_btn = Button(root, text="Add Image", command=select_image)
add_image_btn.pack(pady=20)

# Create 'Generate ID Cards' button
generate_id_cards_btn = Button(root, text="Generate ID Cards", command=generate_id_cards)
generate_id_cards_btn.pack()

# Start GUI event loop
root.mainloop()