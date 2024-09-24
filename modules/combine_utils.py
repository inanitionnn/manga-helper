import os
from PIL import Image  # Pillow
import fitz  # PyMuPDF
from modules.log_utils import log_header_with_time, error_with_time, log_items_with_time, log_path_with_time


def combine_pdfs_to_pdf(folder_path):
    log_header_with_time("Combining")

    pdf_files = sorted([file for file in os.listdir(
        folder_path) if file.endswith('.pdf')])
    if not pdf_files:
        error_with_time("No PDFs found in the specified folder.")
        return

    folder_name = os.path.basename(folder_path)
    output_pdf_name = os.path.splitext(pdf_files[0])[0] + "_combined.pdf"
    output_pdf = os.path.join(folder_path, output_pdf_name)

    log_path_with_time(f"From: '{folder_path}'")
    log_path_with_time(f"To: '{output_pdf_name}'")

    combined_pdf = fitz.open()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        pdf_document = fitz.open(pdf_path)
        combined_pdf.insert_pdf(pdf_document)

    combined_pdf.save(output_pdf)
    combined_pdf.close()

    log_items_with_time(f"Created: {folder_name}_combined.pdf")
    log_header_with_time("End")


def combine_images_to_pdf(folder_path, is_log=True):
    if is_log:
        log_header_with_time("Combining")

    combined_pdf_folder = os.path.join(
        os.path.dirname(folder_path), "combined pdf")
    os.makedirs(combined_pdf_folder, exist_ok=True)

    folder_name = os.path.basename(folder_path)
    output_pdf = os.path.join(combined_pdf_folder, f"{folder_name}.pdf")

    if is_log:
        log_path_with_time(f"From: '{folder_path}'")
        log_path_with_time(f"To: '{os.path.dirname(folder_path)}'")

    # Gather all image files from the folder and sort them
    images = sorted([file for file in os.listdir(folder_path) if file.endswith(
        ('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
    if not images:
        error_with_time("No images found in the specified folder.")
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

    log_items_with_time(f"Created: {folder_name}.pdf")
    if is_log:
        log_header_with_time("End")


def combine_subfolders_images_to_pdfs(folder_path):
    log_header_with_time("Combining")

    log_path_with_time(f"From: '{folder_path}'")

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            log_items_with_time(f"Processing folder: '{item}'")
            combine_images_to_pdf(item_path, False)

    log_header_with_time("End")
