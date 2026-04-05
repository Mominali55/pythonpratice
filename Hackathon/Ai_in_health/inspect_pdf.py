import fitz

def inspect(file_path):
    print(f"Inspecting {file_path}")
    doc = fitz.open(file_path)
    print("Total pages:", len(doc))
    for i, page in enumerate(doc):
        images = page.get_images()
        print(f"Page {i} has {len(images)} images.")
inspect(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\Project_planning.pdf")
inspect(r"C:\Users\momin\Harvard\HarvardSQL\Hackathon\Ai_in_health\More_information_on_project.pdf")
