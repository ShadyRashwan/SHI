
# Author: Shady Rashwan
# 12 March 2023


##############################################
# Complete version works for all image files including .heic on mac
##############################################

import os
from pillow_heif import register_heif_opener
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# warning message 
warning="\n***********************\nPlease note that images will be deleted after processing, only pdf file contains the images will be saved!\nmake a copy of your folder if it's required to retain the images\n***********************\n"


# Register HEIF opener
register_heif_opener()

def load_image(image_file_path):
    try:
        # Load the image
        image = Image.open(image_file_path)
        return image
    except Exception as e:
        # Handle error loading image
        print(f"Error loading image {image_file_path}: {e}")
        return None

def convert_to_png(image_file, image_files):
    # Convert image to PNG
    if image_file.lower().endswith('.heic'):
        image = load_image(image_file)
        if image:
            png_file = os.path.splitext(image_file)[0] + ".png"
            image.save(png_file)
            image_files.append(png_file)
            print(f"Converting .heic {image_file} to {png_file}")
            print("-----------------------\n")
    else:
        image_files.append(image_file)

def create_pdf_from_images(folder_path):
    image_files = []
    print(f"Processing images in folder: {folder_path}")
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            # Recursively process subfolders
            create_pdf_from_images(file_path)
        elif any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic']):
            convert_to_png(file_path, image_files)

    if not image_files:
        print(f"No image files found in {folder_path}")
        return

    folder_name = os.path.basename(folder_path)
    pdf_file = os.path.join(folder_path, f'{folder_name}.pdf')
    c = canvas.Canvas(pdf_file, pagesize=letter)
    image_width = letter[0]
    image_height = letter[1]
    image_files.sort()
    for image_file in image_files:
        # Draw images onto PDF
        c.drawImage(image_file, 0, 0, width=image_width, height=image_height)
        c.showPage()
    c.save()
    print('*****************************************')
    print('Finished creating:', pdf_file.replace(folder_path + '/', ''))
    print('*****************************************\n')

    # Delete image files
    delete_image_files(folder_path)

def delete_image_files(folder_path):
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic']):
                os.remove(file_path)
        print('*****************************************')        
        print("Image files deleted.")
        print('*****************************************\n')
    except Exception as e:
        print(f"Error deleting image files:", e)

def main():
    print(warning)
    parent_folder = input("Enter the path to the parent folder: ")
    if not os.path.exists(parent_folder):
        print("Invalid path to the parent folder.")
        return
    
    create_pdf_from_images(parent_folder)
    print('########################################')
    print("Task completed :Your PDF is ready now! ")
    print('########################################\n')

if __name__ == "__main__":
    main()
