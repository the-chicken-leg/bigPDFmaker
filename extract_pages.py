# /// script
# requires-python = "==3.13.*"
# dependencies = [
#     "pypdf[full]>=6.9.2",
# ]
# ///

from pathlib import Path
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from pypdf import PdfWriter

def main():
    # select source file
    input_path_str = ""
    while not input_path_str:
        input("\nPress Enter key to select a PDF.")
        input_path_str = askopenfilename(
            defaultextension="pdf",
            filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")],
        )
    input_path = Path(input_path_str)
    print(f"Selected PDF: {input_path}")

    # enter pages to extract
    while True:
        pages = input(PAGES_PROMPT)
        try:
            page_list = parse_pages(pages)
            break
        except Exception as err:
            print(f"Error: invalid page input: {err}")

    # select destination filepath
    output_path_str = ""
    while not output_path_str:
        input("\nPress Enter key to select save location.")
        output_path_str = asksaveasfilename(
            defaultextension="pdf",
            filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")],
        )
    output_path = Path(output_path_str)
    print(f"Selected save location: {output_path}")

    # add pages to writer
    print("\nCreating new PDF...")
    writer = PdfWriter()
    num_pages = 0
    for page in page_list:
        try:
            writer.append(input_path, pages=[page], import_outline=False)
            num_pages += 1
        except Exception as err:
            print(f"Error adding page {page + 1} to new PDF: {err}")

    # write writer
    with output_path.open(mode="wb") as output_file:
        writer.write(output_file)
    print(f"New PDF created. {num_pages} pages included.\n")

PAGES_PROMPT = """
Which pages should be extracted and combined? The original PDF will not be modified. 

You can enter:
    - single pages separated by commas: 2, 12, 15
    - a page range with a dash: 4-8
    - a combination of single pages and page ranges separated by commas: 2, 4-8, 12, 15

The pages will be combined in the order you input them: 15, 12, 8-4, 2 is the reverse of 2, 4-8, 12, 15.

You can add a page more than once: 2, 3, 2, 4

Enter pages: """

def parse_pages(pages: str) -> list[int]:
    page_list: list[int] = []
    for page_range in [page_range.strip() for page_range in pages.split(",")]:
        if not page_range:
            continue
        if "-" in page_range:
            parts = page_range.split("-")
            if len(parts) != 2:
                raise Exception("too many dashes")
            
            left, right = int(parts[0]), int(parts[1])
            if left < 1 or right < 1:
                raise Exception("page numbers must be 1 or greater")
            
            if left < right:
                page_list.extend(range(left - 1, right, 1))
            elif left > right:
                page_list.extend(range(left - 1, right - 2, -1))
            elif left == right:
                page_list.append(left - 1)
        else:
            if int(page_range) < 1:
                raise Exception("page numbers must be 1 or greater")
            page_list.append(int(page_range) - 1)

    return page_list

if __name__ == "__main__":
    main()
