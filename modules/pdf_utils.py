
import os
import io
import time
import re
from PIL import Image  # Pillow
import fitz  # PyMuPDF
import rarfile
from zipfile import ZipFile
from tqdm import tqdm
from modules.log_utils import get_error_with_time, get_log_header_with_time, get_log_items_with_time, get_log_path_with_time

def is_locked(filepath):
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                locked = False
        except IOError as message:
            locked = True
        finally:
            if file_object:
                file_object.close()
    return locked

def wait_for_file(filepath):
    wait_time = 1
    while is_locked(filepath):
        time.sleep(wait_time)


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]


def convert_cbz_to_pdf(folder_path):
    print(get_log_header_with_time("Converting"))
    archive_folder_path = os.path.join(folder_path, "archives")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(pdf_folder_path, exist_ok=True)

    print(get_log_path_with_time(f"From: '{archive_folder_path}'"))
    print(get_log_path_with_time(f"To:   '{pdf_folder_path}'"))
    print()

    files = [f for f in os.listdir(archive_folder_path) if f.lower().endswith(('.cbz', '.cbr'))]
    
    with tqdm(total=len(files), desc="Converting", unit="file") as pbar:
        for idx, file_name in enumerate(files):
            archive_path = os.path.join(archive_folder_path, file_name)
            pdf_path = os.path.join(pdf_folder_path, file_name.rsplit('.', 1)[0] + '.pdf')

            if os.path.exists(pdf_path):
                pbar.write(get_log_items_with_time(f"Already converted: '{file_name.rsplit('.', 1)[0] + '.pdf'}'"))
                pbar.update(1)
                continue

            if file_name.lower().endswith('.cbz'):
                with ZipFile(archive_path, 'r') as zip_ref:
                    image_names = [name for name in zip_ref.namelist() if name.lower().endswith(('png', 'jpg', 'jpeg'))]
                    image_names.sort(key=natural_sort_key)

                    images = []
                    for name in image_names:
                        with zip_ref.open(name) as image_file:
                            image_data = io.BytesIO(image_file.read())
                            images.append(Image.open(image_data))

                    if images:
                        images[0].save(pdf_path, save_all=True, append_images=images[1:], optimize=True)
                    for img in images:
                        img.close()

            elif file_name.lower().endswith('.cbr'):
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    image_names = [name for name in rar_ref.namelist() if name.lower().endswith(('png', 'jpg', 'jpeg'))]
                    image_names.sort(key=natural_sort_key)

                    images = []
                    for name in image_names:
                        image_file_path = rar_ref.open(name).name
                        wait_for_file(image_file_path)

                        with rar_ref.open(name) as image_file:
                            image_data = io.BytesIO(image_file.read())
                            try:
                                images.append(Image.open(image_data))
                            except Exception as e:
                                pbar.write(get_error_with_time(f"Error opening image '{name}': {e}"))

                    if images:
                        images[0].save(pdf_path, save_all=True, append_images=images[1:], optimize=True)
                    for img in images:
                        img.close()

            pbar.write(get_log_items_with_time(f"Converted: '{file_name}' to '{file_name.rsplit('.', 1)[0] + '.pdf'}'"))
            pbar.update(1)

    print(get_log_header_with_time("End Converting"))


def compress_pdfs(folder_path):
    print(get_log_header_with_time("Compressing"))

    compressed_pdf_folder_path = os.path.join(folder_path, "compressed")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(compressed_pdf_folder_path, exist_ok=True)

    print(get_log_path_with_time(f"From: '{pdf_folder_path}'"))
    print(get_log_path_with_time(f"To:   '{compressed_pdf_folder_path}'"))
    print()

    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.lower().endswith('.pdf')]

    with tqdm(total=len(pdf_files), desc="Compressing", unit="file") as pbar:
        for file_name in pdf_files:
            pdf_path = os.path.join(pdf_folder_path, file_name)
            compressed_pdf_path = os.path.join(
                compressed_pdf_folder_path, file_name)

            if os.path.exists(compressed_pdf_path):
                pbar.write(get_log_items_with_time(f"Already compressed: '{file_name}'"))
                pbar.update(1)
                continue

            try:
                doc = fitz.open(pdf_path)
                doc.save(compressed_pdf_path,
                         deflate=True,
                         deflate_images=True,
                         deflate_fonts=True,
                         clean=True,
                         garbage=4
                         )
                doc.close()

                pbar.write(get_log_items_with_time(f"Compressed: '{file_name}'"))
            except Exception as e:
                pbar.write(get_error_with_time(f"Error compressing '{file_name}': {e}"))

            pbar.update(1)

    print(get_log_header_with_time("End Compressing"))