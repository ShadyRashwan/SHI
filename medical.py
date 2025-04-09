
# Author: Shady Rashwan
# 12 March 2023


##############################################
# Complete version works for all image files including .heic on mac
##############################################

import os
import math
from pillow_heif import register_heif_opener
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm

# Image extensions supported
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic']

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

def convert_to_png(image_file, image_files, temp_files=[]):
    # Convert image to PNG
    if image_file.lower().endswith('.heic'):
        image = load_image(image_file)
        if image:
            png_file = os.path.splitext(image_file)[0] + ".png"
            image.save(png_file)
            image_files.append(png_file)
            temp_files.append(png_file)  # Track converted files separately
            print(f"Converting .heic {image_file} to {png_file}")
            print("-----------------------\n")
    else:
        image_files.append(image_file)

def fit_image_to_page(image_path, c, page_width, page_height):
    """Resize and center image maintaining aspect ratio"""
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    # Calculate scale factors for width and height
    width_scale = page_width / img_width
    height_scale = page_height / img_height
    
    # Use the smaller scale factor to ensure the image fits on the page
    scale = min(width_scale, height_scale)
    
    # Calculate new dimensions
    new_width = img_width * scale
    new_height = img_height * scale
    
    # Calculate position to center the image on page
    x_pos = (page_width - new_width) / 2
    y_pos = (page_height - new_height) / 2
    
    # Draw the image on the page
    c.drawImage(image_path, x_pos, y_pos, width=new_width, height=new_height)

def create_pdf_from_images(folder_path, preserve_originals=False):
    image_files = []
    temp_files = []  # Track files created during conversion for cleanup
    
    # Collect all image files in the folder
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                all_files.append(file_path)
    
    # Process only files in the current folder, not subfolders
    print(f"Processing images in folder: {folder_path}")
    current_folder_files = [f for f in all_files if os.path.dirname(f) == folder_path]
    
    # Use tqdm for progress bar
    for file_path in tqdm(current_folder_files, desc="Processing images"):
        if any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            convert_to_png(file_path, image_files, temp_files)
    
    # Process subfolders recursively
    for item in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, item)
        if os.path.isdir(subfolder_path):
            create_pdf_from_images(subfolder_path, preserve_originals)

    if not image_files:
        print(f"No image files found in {folder_path}")
        return

    folder_name = os.path.basename(folder_path)
    pdf_file = os.path.join(folder_path, f'{folder_name}.pdf')
    c = canvas.Canvas(pdf_file, pagesize=letter)
    page_width, page_height = letter
    
    image_files.sort()
    for image_file in tqdm(image_files, desc="Creating PDF"):
        # Draw images onto PDF with proper sizing
        fit_image_to_page(image_file, c, page_width, page_height)
        c.showPage()
    c.save()
    print('*****************************************')
    print('Finished creating:', pdf_file.replace(folder_path + '/', ''))
    print('*****************************************\n')

    # Delete image files if not preserving originals
    if not preserve_originals:
        # Only delete temporary converted files in any case
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        # Delete original files if not preserving
        delete_image_files(folder_path)

def delete_image_files(folder_path):
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                os.remove(file_path)
        print('*****************************************')        
        print("Image files deleted.")
        print('*****************************************\n')
    except Exception as e:
        print(f"Error deleting image files:", e)

def print_welcome_message():
    """Display a decorated welcome message with tool information"""
    welcome = r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                ███████╗██╗  ██╗██╗                               ║
║                ██╔════╝██║  ██║██║                               ║
║                ███████╗███████║██║                               ║
║                ╚════██║██╔══██║██║                               ║
║                ███████║██║  ██║██║                               ║
║                ╚══════╝╚═╝  ╚═╝╚═╝                               ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  IMAGES TO PDF CONVERTER                                         ║
║                                                                  ║
║  • Automatically converts images in folders to PDF               ║
║  • Preserves image aspect ratios                                 ║
║  • Works with HEIC and all common image formats                  ║
║  • Processes subfolders recursively                              ║
║                                                                  ║
║  Author: Shady Rashwan                                           ║
║  Version: 2.0                                                    ║
║  Date: March 2023                                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(welcome)

    # Warning message
    warning = """
⚠️  IMPORTANT NOTE ⚠️
By default, images will be deleted after processing.
Only the PDF file containing the images will be saved!
"""
    print(warning)


def print_completion_message(folder_name):
    """Display a decorated completion message"""
    completion = f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                     🎉  TASK COMPLETED!  🎉                      ║
║                                                                  ║
║  Your PDF has been successfully created in:                      ║
║  {folder_name}                                 
║                                                                  ║
║  Thank you for using the tool!                                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(completion)


def main():
    print_welcome_message()
    
    parent_folder = input("Enter the path to the parent folder: ")
    
    # Strip any quotes from the path that might have been copied/pasted
    parent_folder = parent_folder.strip('\'"')
    
    if not os.path.exists(parent_folder):
        print(f"Invalid path to the parent folder: '{parent_folder}'")
        print("Tips: Make sure the path exists and you have permissions to access it.")
        print("If you copied the path, ensure there are no extra quotes or spaces.")
        return
    
    preserve = input("Do you want to preserve original images? (y/n): ").lower().startswith('y')
    
    create_pdf_from_images(parent_folder, preserve_originals=preserve)
    print_completion_message(parent_folder)

if __name__ == "__main__":
    main()
