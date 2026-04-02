from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory

import writers

def main():
    # get input directory
    input_directory = None
    while not input_directory:
        input("Press Enter key to select a folder.")
        input_directory = askdirectory(mustexist=True)
    input_directory = Path(input_directory)
    print(f"Selected folder:        {input_directory}\n")

    # get output path
    output_path = None
    while not output_path:
        input("Press Enter key to select save location.")
        output_path = asksaveasfilename(
                defaultextension="pdf",
                filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")],
        )
    output_path = Path(output_path)
    print(f"Selected save location: {output_path}\n")

    # create big PDF
    print("Creating big PDF. This might take a few minutes...")
    writer, added_to_big_pdf = writers.create_writer(input_directory)
    writers.write_writer(writer, added_to_big_pdf, output_path)
    # writers.write_writer(writers.compress_writer(writer), added_to_big_pdf, output_path)    # compression broken
    num_files = len(added_to_big_pdf)
    print(f"Big PDF created. {num_files} PDFs included.")

if __name__ == "__main__":
    main()
