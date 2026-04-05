from pdfminer.high_level import extract_text

def main():
    try:
        t1 = extract_text(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\Project_planning.pdf")
        with open(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\pdf1.txt", "w", encoding="utf-8") as f:
            f.write(t1)
    except Exception as e:
        print("Error pdf1", e)
        
    try:
        t2 = extract_text(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\More_information_on_project.pdf")
        with open(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\pdf2.txt", "w", encoding="utf-8") as f:
            f.write(t2)
    except Exception as e:
        print("Error pdf2", e)

if __name__ == "__main__":
    main()
