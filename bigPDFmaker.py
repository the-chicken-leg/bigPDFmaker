# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pypdf[full]>=6.9.2",
# ]
# ///
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
# from itertools import islice    # use for testing slices

from pypdf import PdfWriter

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
    writer, added_to_big_pdf = create_writer(input_directory)
    write_writer(writer, added_to_big_pdf, output_path)
    # writers.write_writer(writers.compress_writer(writer), added_to_big_pdf, output_path)    # compression broken
    num_files = len(added_to_big_pdf)
    print(f"Big PDF created. {num_files} PDFs included.")

def create_writer(glob_dir: Path):
    glob_sort = sorted(
        glob_dir.glob("*.pdf"),
        key=lambda filepath: filepath.name.lower(),
    )
    glob_dedup = {filepath.name: filepath for filepath in glob_sort}    # this doesn't do anything useful now, but would be useful for dedeplication for a future rglob use case

    writer = PdfWriter()
    added_to_big_pdf = []
    # for filepath in islice(glob_dedup.values(), 10):    # use for testing slices
    for filepath in glob_dedup.values():
        try:
            current_page = writer.get_num_pages()
            writer.append(filepath, import_outline=False)
            writer.add_outline_item(title=filepath.name, page_number=current_page)
            added_to_big_pdf.append(filepath.name + "\n")
        except Exception as err:
            print(f"Error adding {filepath.name} to big PDF: {err}")
            continue

    return writer, added_to_big_pdf

def compress_writer(writer: PdfWriter):
    for page in writer.pages:
        page.compress_content_streams(level=9)
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    
    return writer

def write_writer(writer: PdfWriter, added_to_big_pdf: list, pdf_output_path: Path):
    with pdf_output_path.open(mode="wb") as output_file:
        writer.write(output_file)

    contents_output_path = pdf_output_path.parent / f"{pdf_output_path.name}_contents.txt"
    with contents_output_path.open(mode="w", encoding="utf-8") as output_file:
        output_file.writelines(added_to_big_pdf)

if __name__ == "__main__":
    main()
