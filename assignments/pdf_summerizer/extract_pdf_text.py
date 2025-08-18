from PyPDF2 import PdfReader
from agents import function_tool

@function_tool
def extract_pdf_text(file_path:str)-> str:
    """
        Reads and extracts text from a PDF file.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            str: Extracted text from the PDF.
    """
    if not file_path.lower().endswith('.pdf'):
        return "Error: The file is not a PDF."
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error reading PDF file: {e}"
    
    
# if __name__ == "__main__":
#     read_pdf("filepath.pdf")
