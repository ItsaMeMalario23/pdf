from pypdf import PdfReader, PdfWriter
import os.path
import sys

#   Python 3.13.1
#   pypdf  5.3.1

# save output file containing page
def saveFile(name: str, writer: PdfWriter) -> None:
    if not name:
        print(f"[ERROR]: Failed to save file, name is null")
        return
    
    if writer is None:
        print(f"[ERROR]: Failed to save file {name}, file data is null")
        return

    with open("output/" + name.strip() + ".pdf", "wb") as outputfd:
        writer.write(outputfd)


# get output filename from page
def getFileName(reader: PdfReader, pageIdx: int) -> str:
    numPages: int = reader.get_num_pages()

    if numPages == 0:
        print(f"[ERROR]: Input file empty")
        return None
    
    if pageIdx >= numPages:
        print(f"[ERROR]: Page index {pageIdx + 1} out of bounds")
        return None

    text: str = reader.pages[pageIdx].extract_text()
    idx: int = text.find("Kst.: ") + 6

    if idx < 0:
        print(f"[ERROR]: No Kst identifier found on page {pageIdx + 1}")
        return None
    
    len: int = idx

    while text[len].isdigit():
        len += 1

    if len - idx > 5 or len - idx < 2:
        print(f"[WARNING]: Invalid Kst value length {len} on page {pageIdx + 1}, ignoring page")
        return None
    
    return text[idx:len]


# open input file
def openFile(filename: str) -> PdfReader:
    if not filename:
        print(f"[ERROR]: Empty file name")
        exit(-1)

    if os.path.isfile(filename) == False:
        print(f"[ERROR]: File {filename} not found")
        exit(-1)
    
    if ".pdf" not in filename.lower():
        print(f"[ERROR]: File {filename} is not a PDF file")
        exit(-1)
    
    return PdfReader(filename)


def main():
    argc: int = len(sys.argv)

    if argc < 2:
        print(f"[ERROR]: No file name specified")
        exit(-1)

    if argc > 2:
        print(f"[WARNING]: Multiple arguments passed, only first argument will be processed")

    inputfname: str = sys.argv[1].strip()
    outputfname: str = ""
    next: str = None

    reader: PdfReader = openFile(inputfname)
    writer: PdfWriter = PdfWriter()

    if reader is not None:
        print(f"Processing file \"{inputfname}\"\n")

    numpages: int = 0
    errcount: int = 0

    for i in range(0, reader.get_num_pages()):
        next = getFileName(reader, i)

        if next is None:
            errcount += 1
            continue

        if next != outputfname and numpages > 0:
            saveFile(outputfname, writer)
            print(f"Saved {numpages} page(s) to file {outputfname}.pdf")

            writer = PdfWriter()
            numpages = 0

        writer.add_page(reader.pages[i])

        outputfname = next
        numpages += 1

    if numpages > 0:
        saveFile(outputfname, writer)
        print(f"Saved {numpages} page(s) to file {outputfname}.pdf")

    if errcount == 0:
        print(f"\nAll pages of input file \"{inputfname}\" were processed successfully\n")
    else:
        print(f"\nFailed to process {errcount} page(s) from input file \"{inputfname}\"\n")


if __name__ == "__main__":
    main()