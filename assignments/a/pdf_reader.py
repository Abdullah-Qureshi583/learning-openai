from PyPDF2 import PdfReader

def read_pdf(file_path):
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
