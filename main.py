from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory

import writers

def main():
    input(
"""This Python CLI program combines PDF documents from a folder (non-recursively) into a big PDF (sorted by filename).

Bookmarks will be created for each document added to the big PDF.

Press Enter key to select a folder."""
    )
    input_directory = askdirectory(mustexist=True)
    if not input_directory:
        return
    else:
        input_directory = Path(input_directory)
        print(f"Selected folder: {input_directory}")

    get_filename_and_save(input_directory)
    input("Press Enter key to exit.")
    print("Cleaning up...") 

def get_filename_and_save(input_directory: Path):
    input("\nPress Enter key to select save location.")
    output_path = asksaveasfilename(
            defaultextension="pdf",
            filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")],
    )
    if not output_path:
        return
    else:
        output_path = Path(output_path)
        print(f"Selected save location: {output_path}")

    print("\nCreating big PDF. This might take a few minutes...")
    writer, added_to_big_pdf = writers.create_writer(input_directory)
    writers.write_writer(writer, added_to_big_pdf, output_path)
    # writers.write_writer(writers.compress_writer(writer), added_to_big_pdf, output_path)      # compression broken
    num_files = len(added_to_big_pdf)
    print(f"\nBig PDF created. {num_files} PDFs included.")

if __name__ == "__main__":
    main()