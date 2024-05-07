from PIL import Image, ImageDraw, ImageFont
import csv

def create_id_card(template_path, photo_path, name, position, output_path):
    # Load the ID card template
    id_card = Image.open(template_path)

    # Load the user's photo
    photo = Image.open(photo_path)

    # Resize the photo to fit the ID card template
    photo = photo.resize((100, 100))  # Adjust size as needed

    # Paste the photo onto the ID card template
    id_card.paste(photo, (20, 20))  # Adjust coordinates as needed

    # Draw the text onto the ID card
    draw = ImageDraw.Draw(id_card)
    font = ImageFont.truetype('arial.ttf', size=30)  # Adjust font and size as needed
    draw.text((150, 20), name, fill='black', font=font)  # Adjust coordinates as needed
    draw.text((150, 70), position, fill='black', font=font)  # Adjust coordinates as needed

    # Save the final ID card
    id_card.save(output_path)

# Read the CSV file
with open('employees.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        name, position, photo_path = row
        output_path = f'{name}_id_card.png'
        create_id_card('id_template.png', photo_path, name, position, output_path)
