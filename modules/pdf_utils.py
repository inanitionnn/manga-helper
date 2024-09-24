import os
import re
from PIL import Image  # Pillow
import fitz  # PyMuPDF
from zipfile import ZipFile
from modules.log_utils import log_header_with_time, log_items_with_time, log_path_with_time


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def convert_cbz_to_pdf(folder_path):
    log_header_with_time("Converting")
    cbz_folder_path = os.path.join(folder_path, "cbz")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(pdf_folder_path, exist_ok=True)

    log_path_with_time(f"From: '{cbz_folder_path}'")
    log_path_with_time(f"To: '{pdf_folder_path}'")

    for file_name in os.listdir(cbz_folder_path):
        if file_name.lower().endswith('.cbz'):
            cbz_path = os.path.join(cbz_folder_path, file_name)
            pdf_path = os.path.join(
                pdf_folder_path, file_name.replace(
                    '.cbz', '.pdf'))

            if os.path.exists(pdf_path):
                log_items_with_time(
                    f"Already converted: '{
                        file_name.replace(
                            '.cbz', '.pdf')}'")
                continue

            with ZipFile(cbz_path, 'r') as zip_ref:
                # Extract image file names and sort them naturally
                image_names = [
                    name for name in zip_ref.namelist() if name.lower().endswith(
                        ('png', 'jpg', 'jpeg'))]
                image_names.sort(key=natural_sort_key)

                # Open images in sorted order
                images = [Image.open(zip_ref.open(name))
                          for name in image_names]
                if images:  # Save images as a single PDF file
                    images[0].save(pdf_path, save_all=True,
                                   append_images=images[1:], optimize=True)
            log_items_with_time(
                f"Converted: '{file_name}' to '{file_name.replace('.cbz', '.pdf')}'")

    log_header_with_time("End")


def compress_pdfs(folder_path):
    log_header_with_time("Compressing")

    compressed_pdf_folder_path = os.path.join(folder_path, "compressed pdf")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(compressed_pdf_folder_path, exist_ok=True)

    log_path_with_time(f"From: '{pdf_folder_path}'")
    log_path_with_time(f"To: '{compressed_pdf_folder_path}'")

    for file_name in os.listdir(pdf_folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file_name)
            compressed_pdf_path = os.path.join(
                compressed_pdf_folder_path, file_name)

            if os.path.exists(compressed_pdf_path):
                log_items_with_time(f"Already compressed: '{file_name}'")
                continue

            doc = fitz.open(pdf_path)
            doc.save(compressed_pdf_path,
                     deflate=True,
                     deflate_images=True,
                     deflate_fonts=True,
                     clean=True,
                     garbage=4
                     )
            doc.close()

            log_items_with_time(f"Compressed: '{file_name}'")

    log_header_with_time("End")
