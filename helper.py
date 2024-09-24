import os
from modules.log_utils import log_header_with_time, input_with_time, log_with_time, error_with_time
from modules.combine_utils import combine_pdfs_to_pdf, combine_subfolders_images_to_pdfs
from modules.file_utils import move_files_to_subfolders, rename_files, remove_subfolders
from modules.pdf_utils import compress_pdfs, convert_cbz_to_pdf


def print_menu():
    log_header_with_time("Choose an action")
    log_with_time("   0. Exit")
    log_with_time("   1. Print menu")
    log_with_time("   2. Enter new directory path")
    log_with_time("   --------------------------------------")
    log_with_time("   3. Rename files")
    log_with_time("   4. Move files to subfolders")
    log_with_time("   5. Remove subfolders")
    log_with_time("   --------------------------------------")
    log_with_time("   6. Convert files")
    log_with_time("   7. Compress files")
    log_with_time("   --------------------------------------")
    log_with_time("   8. Combine subfolders images")
    log_with_time("   9. Combine pdf files in a folder")
    log_with_time("   --------------------------------------")


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
        try:
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
                move_files_to_subfolders(directory_path)
            elif choice == "5":
                remove_subfolders(directory_path)
            elif choice == "6":
                convert_cbz_to_pdf(directory_path)
            elif choice == "7":
                compress_pdfs(directory_path)
            elif choice == "8":
                combine_subfolders_images_to_pdfs(directory_path)
            elif choice == "9":
                combine_pdfs_to_pdf(directory_path)
            elif choice == "0":
                log_header_with_time("Exiting...")
                break
            else:
                error_with_time("Invalid choice. Please enter a valid number.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_with_time(e)


if __name__ == "__main__":
    main()
