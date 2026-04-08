# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pypdf[full]>=6.9.2",
# ]
# ///

from pathlib import Path
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
import argparse
# from itertools import islice    # use for testing slices

from pypdf import PdfWriter

# argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-b", "--bookmarks",
    action="store_true",
    help="create PDF bookmarks",
)
parser.add_argument(
    "-m", "--manifest",
    action="store_true",
    help="create .txt manifest",
)
args = parser.parse_args()

# get input directory
input_directory_str = ""
print()
while not input_directory_str:
    input("Press Enter key to select a folder.")
    input_directory_str = askdirectory(mustexist=True)
input_directory = Path(input_directory_str)
print(f"Selected folder:        {input_directory}\n")

# get output path
output_path_str = ""
while not output_path_str:
    input("Press Enter key to select save location.")
    output_path_str = asksaveasfilename(
            defaultextension="pdf",
            filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")],
    )
output_path = Path(output_path_str)
print(f"Selected save location: {output_path}\n")

# create writer
print("Creating big PDF...")

glob_sort = sorted(
    input_directory.glob("*.pdf"),
    key=lambda filepath: filepath.name.lower(),
)
glob_dedup = {filepath.name: filepath for filepath in glob_sort}    # this doesn't do anything useful now, but would be useful for dedeplication for a future rglob use case

writer = PdfWriter()
added_to_big_pdf: list[str] = []
# for filepath in islice(glob_dedup.values(), 10):    # use for testing slices
for filepath in glob_dedup.values():
    try:
        current_page = writer.get_num_pages()
        writer.append(filepath, import_outline=False)
        if args.bookmarks:
            writer.add_outline_item(title=filepath.name, page_number=current_page)
        added_to_big_pdf.append(filepath.name + "\n")
    except Exception as err:
        print(f"Error adding {filepath.name} to big PDF: {err}")

# compress writer (broken)
# for page in writer.pages:
#     page.compress_content_streams(level=9)
# writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

# write writer
with output_path.open(mode="wb") as output_file:
    writer.write(output_file)

if args.manifest:
    manifest_output_path = output_path.parent / f"{output_path.name}_manifest.txt"
    with manifest_output_path.open(mode="w", encoding="utf-8") as output_file:
        output_file.writelines(added_to_big_pdf)

num_files = len(added_to_big_pdf)
print(f"Big PDF created. {num_files} PDFs included.\n")
