import fitz  # PyMuPDF
import os

from modules.log_utils import log_header_with_time, log_items_with_time, log_path_with_time


def reverse_pdf(input_pdf: str, output_pdf: str, is_log=True):
    if is_log:
        log_header_with_time("Reversing PDF")
        log_path_with_time(f"From: '{input_pdf}'")
        log_path_with_time(f"To: '{output_pdf}'")

    doc = fitz.open(input_pdf)
    reversed_doc = fitz.open()

    for page_num in range(doc.page_count - 1, -1, -1):
        page = doc.load_page(page_num)
        reversed_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    reversed_doc.save(output_pdf)
    reversed_doc.close()
    doc.close()

    if is_log:
        log_items_with_time(f"Reversed: '{output_pdf}'")
        log_header_with_time("End")


def reverse_pdfs_in_folder(folder_path: str):
    log_header_with_time("Reversing")

    log_path_with_time(f"From: '{folder_path}'")

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            input_pdf = os.path.join(folder_path, filename)
            output_pdf = os.path.join(
                folder_path, f"{
                    os.path.splitext(filename)[0]}-reversed.pdf")

            reverse_pdf(input_pdf, output_pdf, False)
            log_items_with_time(f"Reversed '{filename}'")

    log_header_with_time("End")
