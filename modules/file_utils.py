import os
import re
import shutil

from modules.log_utils import log_header_with_time, input_with_time, error_with_time, log_items_with_time, log_path_with_time


def rename_files(folder_path):
    log_header_with_time("Renaming")
    log_path_with_time(f"In: '{folder_path}'")

    new_name = input_with_time("new file name")
    renamed_files_count = 0

    # PS: Any suggestions for further improvement are welcome.

    volume_patterns = [
        r'v(\d+)',              # Matches v01, v08, etc.
        r'Volume[_ ]?(\d+)',    # Matches Volume_06, Volume 06, etc.
        r'(\d{1,3})'            # Matches simple volume numbers (e.g., 3)
    ]

    # Get list of files, excluding directories
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # If only one file exists, rename without pattern
    if len(files) == 1:
        file_name = files[0]
        full_path = os.path.join(folder_path, file_name)
        new_file_name = f"{new_name}.{file_name.split('.')[-1].lower()}"
        new_path = os.path.join(folder_path, new_file_name)

        try:
            os.rename(full_path, new_path)
            log_items_with_time(f"Renamed: '{file_name}' to '{new_file_name}'")
            return
        except Exception as e:
            error_with_time(f"Could not rename '{file_name}' due to an error: {e}")
            return

    # Proceed with renaming if more than one file
    for file_name in os.listdir(folder_path):
        try:
            full_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(full_path):
                continue  # Skip directories

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

    log_header_with_time("End Renaming")


def move_files_to_subfolders(folder_path):
    log_header_with_time("Moving")

    archive_folder_path = os.path.join(folder_path, "archives")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    os.makedirs(archive_folder_path, exist_ok=True)
    os.makedirs(pdf_folder_path, exist_ok=True)

    log_path_with_time(f"From: '{folder_path}'")

    for filename in os.listdir(folder_path):
        source_path = os.path.join(folder_path, filename)

        if filename.lower().endswith(('.cbz', '.cbr')):
            destination_path = os.path.join(archive_folder_path, filename)
            shutil.move(source_path, destination_path)
            log_items_with_time(f"Moved to cbz: '{filename}'")
        elif filename.endswith('.pdf'):
            destination_path = os.path.join(pdf_folder_path, filename)
            shutil.move(source_path, destination_path)
            log_items_with_time(f"Moved to pdf: '{filename}'")

    log_header_with_time("End Moving")


def remove_subfolders(folder_path):
    log_header_with_time("Removing")

    # Define folder paths
    archive_folder_path = os.path.join(folder_path, "archives")
    pdf_folder_path = os.path.join(folder_path, "pdf")
    compressed_folder_path = os.path.join(folder_path, "compressed")

    # Move files from 'compressed pdf' to root folder
    if os.path.exists(compressed_folder_path):
        for filename in os.listdir(compressed_folder_path):
            source_path = os.path.join(compressed_folder_path, filename)
            destination_path = os.path.join(folder_path, filename)

            # Move the file to the root folder
            shutil.move(source_path, destination_path)
            log_items_with_time(
                f"Moved file from 'compressed pdf': '{filename}'")

        # Optionally remove the empty 'compressed pdf' folder
        shutil.rmtree(compressed_folder_path)
        log_items_with_time(
            f"Removed folder: '{compressed_folder_path}'")

    # Remove cbz and pdf folders if they exist
    if os.path.exists(archive_folder_path):
        shutil.rmtree(archive_folder_path)
        log_items_with_time(f"Removed folder: '{archive_folder_path}'")

    if os.path.exists(pdf_folder_path):
        shutil.rmtree(pdf_folder_path)
        log_items_with_time(f"Removed folder: '{pdf_folder_path}'")

    log_header_with_time("End Removing")
