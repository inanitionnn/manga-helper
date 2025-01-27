import os
from tqdm import tqdm
from PIL import Image  # Pillow
import fitz  # PyMuPDF
from modules.log_utils import get_error_with_time, get_log_header_with_time, get_log_items_with_time, get_log_path_with_time


def combine_pdfs_to_pdf(folder_path):
    print(get_log_header_with_time("Combining"))

    pdf_files = sorted([file for file in os.listdir(
        folder_path) if file.endswith('.pdf')])
    if not pdf_files:
        print(get_error_with_time("No PDFs found in the specified folder."))
        return

    combined_pdf_folder = os.path.join(folder_path, "pdf")
    os.makedirs(combined_pdf_folder, exist_ok=True)

    folder_name = os.path.basename(folder_path)
    output_pdf = os.path.join(combined_pdf_folder, f"{folder_name}.pdf")

    print(get_log_path_with_time(f"From: '{folder_path}'"))
    print(get_log_path_with_time(f"To:   '{combined_pdf_folder}'"))
    print()

    combined_pdf = fitz.open()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        pdf_document = fitz.open(pdf_path)
        combined_pdf.insert_pdf(pdf_document)

    combined_pdf.save(output_pdf)
    combined_pdf.close()

    print(get_log_items_with_time(f"Created: {folder_name}_combined.pdf"))
    print(get_log_header_with_time("End Combining"))


def combine_images_to_pdf(folder_path):
    combined_pdf_folder = os.path.join(
        os.path.dirname(folder_path), "pdf")
    os.makedirs(combined_pdf_folder, exist_ok=True)

    folder_name = os.path.basename(folder_path)
    output_pdf = os.path.join(combined_pdf_folder, f"{folder_name}.pdf")

    # Gather all image files from the folder and sort them
    images = sorted([file for file in os.listdir(folder_path) if file.endswith(
        ('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
    if not images:
        print(get_error_with_time("No images found in the specified folder."))
        return

    # Open the first image and convert remaining images to RGB mode
    first_image = Image.open(
        os.path.join(
            folder_path,
            images[0])).convert('RGB')
    image_list = [Image.open(os.path.join(folder_path, image)).convert(
        'RGB') for image in images[1:]]

    # Save images as a single PDF file
    first_image.save(output_pdf, save_all=True, append_images=image_list)

    print(get_log_items_with_time(f"Created: {folder_name}.pdf"))


def combine_subfolders_images_to_pdfs(folder_path):
    print(get_log_header_with_time("Combining"))

    print(get_log_path_with_time(f"From: '{folder_path}'"))
    print()

    subfolders = [item for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item))]

    with tqdm(total=len(subfolders), desc="Combining folders", unit="folder") as pbar:
        for item in subfolders:
            item_path = os.path.join(folder_path, item)

            combine_images_to_pdf(item_path)
            
            pbar.write(get_log_items_with_time(f"Already compressed: '{item}'"))
            pbar.update(1)

    print(get_log_header_with_time("End Combining"))
