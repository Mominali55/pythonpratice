import fitz  # PyMuPDF

def read_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading {file_path}: {e}"

if __name__ == "__main__":
    text1 = read_pdf(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\Project_planning.pdf")
    text2 = read_pdf(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\More_information_on_project.pdf")
    with open(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\pdf_output.txt", "w", encoding="utf-8") as f:
        f.write("--- Project_planning.pdf ---\n")
        f.write(text1)
        f.write("\n--- More_information_on_project.pdf ---\n")
        f.write(text2)
