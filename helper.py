import os
import re
import shutil
from PIL import Image  # Pillow
import fitz  # PyMuPDF
from zipfile import ZipFile
from datetime import datetime


def log_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    print(f"[{current_time}] {message}")


def error_with_time(message):
    log_with_time(f"(╥‸╥) {message}")


def log_items_with_time(message):
    log_with_time(f"♡♡♡ {message} ♡♡♡")


def log_path_with_time(message):
    log_with_time(f"{message} ᐟ.⊹.˚୧")


def log_header_with_time(message):
    log_with_time(f"˖⁺‧₊˚♡˚ {message} ˚♡˚₊‧⁺˖")


def input_with_time(message):
    current_time = datetime.now().strftime("%H:%M")
    log_with_time(f"Enter {message} 𖦹 ⋆｡°✩")
    result = input(f"[{current_time}] ===> ").strip()
    return result


def rename_files(folder_path):
    log_header_with_time("Renaming")
    log_path_with_time(f"In: '{folder_path}'")

    new_name = input_with_time("new file name")
    renamed_files_count = 0

    # PS: Any suggestions for further improvement or additional cases are
    # welcome.

    volume_patterns = [
        r'v(\d+)',              # Matches v01, v08, etc.
        r'Volume[_ ]?(\d+)',    # Matches Volume_06, Volume 06, etc.
        r'(\d{1,2})'            # Matches simple volume numbers (e.g., 3)
    ]

    for file_name in os.listdir(folder_path):
        try:
            volume_number = None

            # Find volume number using patterns
            for pattern in volume_patterns:
                match = re.search(pattern, file_name, re.IGNORECASE)
                if match:
                    # Pad volume number with zeros (e.g., 001, 002, etc.)
                    volume_number = match.group(1).zfill(3)
                    break

            if volume_number:  # Create new file name and rename file
                new_file_name = f"{new_name} v{volume_number}.{
                    file_name.split('.')[
                        -1].lower()}"
                old_path = os.path.join(folder_path, file_name)
                new_path = os.path.join(folder_path, new_file_name)

                os.rename(old_path, new_path)
                log_items_with_time(
                    f"Renamed: '{file_name}' to '{new_file_name}'")
                renamed_files_count += 1
            else:
                error_with_time(
                    f"File '{file_name}' does not contain a recognizable volume number and was skipped.")

        except Exception as e:
            error_with_time(
                f"Could not rename '{file_name}' due to an error: {e}")

    if renamed_files_count == 0:
        error_with_time(
            "No files matching the renaming pattern were found in the folder.")

    log_header_with_time("End")


def images_to_pdf(folder_path, is_log=True):
    if is_log:
        log_header_with_time("Creating")

    folder_name = os.path.basename(folder_path)
    output_pdf = os.path.join(
        os.path.dirname(folder_path),
        f"{folder_name}.pdf")

    if is_log:
        log_path_with_time(f"From: '{folder_path}'")
    if is_log:
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


def convert_all_subfolders_to_pdf(parent_folder_path):
    log_header_with_time("Creating")
    print(f"From: '{parent_folder_path}'")
    print(os.listdir(parent_folder_path))
    for item in os.listdir(parent_folder_path):
        item_path = os.path.join(parent_folder_path, item)

        if os.path.isdir(item_path):
            log_items_with_time(f"Processing folder: '{item}'")
            images_to_pdf(item_path, False)

    log_header_with_time("End")


def move_cbz_and_pdf_files(folder_path):
    log_header_with_time("Moving")

    cbz_folder_path = os.path.join(folder_path, "cbz")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(cbz_folder_path, exist_ok=True)
    os.makedirs(pdf_folder_path, exist_ok=True)

    log_path_with_time(f"From: '{folder_path}'")

    for filename in os.listdir(folder_path):
        source_path = os.path.join(folder_path, filename)

        if filename.endswith('.cbz') or filename.endswith('.cbr'):
            destination_path = os.path.join(cbz_folder_path, filename)
            shutil.move(source_path, destination_path)
            log_items_with_time(f"Moved to cbz: '{filename}'")
        elif filename.endswith('.pdf'):
            destination_path = os.path.join(pdf_folder_path, filename)
            shutil.move(source_path, destination_path)
            log_items_with_time(f"Moved to pdf: '{filename}'")

    log_header_with_time("End")


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
                # Extract images from .cbz
                images = [
                    Image.open(
                        zip_ref.open(name)) for name in zip_ref.namelist() if name.lower().endswith(
                        ('png', 'jpg', 'jpeg'))]
                if images:  # Save images as a single PDF file
                    images[0].save(pdf_path, save_all=True,
                                   append_images=images[1:], optimize=True)
            log_items_with_time(
                f"Converted: '{file_name}' to '{
                    file_name.replace(
                        '.cbz', '.pdf')}'")

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


def combine_pdfs(folder_path):
    log_header_with_time("Combining PDFs")

    pdf_files = sorted([file for file in os.listdir(
        folder_path) if file.endswith('.pdf')])
    if not pdf_files:
        error_with_time("No PDFs found in the specified folder.")
        return

    folder_name = os.path.basename(folder_path)
    output_pdf_name = os.path.splitext(pdf_files[0])[0] + "_combined.pdf"
    output_pdf = os.path.join(os.path.dirname(folder_path), output_pdf_name)

    log_path_with_time(f"From: '{folder_path}'")
    log_path_with_time(f"To: '{output_pdf_name}'")

    combined_pdf = fitz.open()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        log_path_with_time(f"Adding: '{pdf_path}'")
        pdf_document = fitz.open(pdf_path)
        combined_pdf.insert_pdf(pdf_document)

    combined_pdf.save(output_pdf)
    combined_pdf.close()

    log_items_with_time(f"Created: {folder_name}_combined.pdf")
    log_header_with_time("End")


def print_menu():
    log_header_with_time("Choose an action")
    log_with_time("   1. Print menu")
    log_with_time("   2. Enter new directory path")
    log_with_time("   3. Rename files in a folder")
    log_with_time(
        "   4. Move files from a folder to 'cbz' and 'pdf' subfolders")
    log_with_time("   5. Covert files from 'cbz' folder to 'pdf' folder")
    log_with_time(
        "   6. Compress files from 'pdf' folder to 'compressed pdf' folder")
    log_with_time("   7. Convert all subfolders with images to pdf files")
    log_with_time("   8. Combine all pdf files in a folder")
    log_with_time("   0. Exit")


def get_directory_path():
    while True:
        directory_path = input_with_time("directory path").strip()
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            return directory_path
        else:
            error_with_time(
                f"Invalid directory path: '{directory_path}'. Please try again.")


def main():
    log_header_with_time("Hello! Let's get started.")
    directory_path = get_directory_path()
    print()
    print_menu()

    while True:
        print()
        choice = input_with_time("your choice")
        print()
        if choice == "1":
            print_menu()
        elif choice == "2":
            directory_path = get_directory_path()
        elif choice == "3":
            rename_files(directory_path)
        elif choice == "4":
            move_cbz_and_pdf_files(directory_path)
        elif choice == "5":
            convert_cbz_to_pdf(directory_path)
        elif choice == "6":
            compress_pdfs(directory_path)
        elif choice == "7":
            convert_all_subfolders_to_pdf(directory_path)
        elif choice == "8":
            combine_pdfs(directory_path)
        elif choice == "0":
            log_header_with_time("Exiting...")
            break
        else:
            error_with_time("Invalid choice. Please enter a valid number.'")


if __name__ == "__main__":
    main()
