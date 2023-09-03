import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTChar, LTText
from pdfminer.converter import PDFPageAggregator


def extract_fonts_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        parser = PDFParser(file)
        document = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        fonts = set()

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            for lobj in layout:
                if isinstance(lobj, LTText):
                    for obj in lobj:
                        if isinstance(obj, LTChar):
                            fonts.add(obj.fontname)

    return sorted(list(fonts))


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    fonts = extract_fonts_from_pdf(pdf_path)
    for font in fonts:
        print(font)
