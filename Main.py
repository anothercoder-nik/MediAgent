from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from Utils.Agents import (
    extract_text_from_pdf, structure_medical_report,
    Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam,
    generate_report_pdf
)

load_dotenv()

pdf_path = "case-report-.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(pdf_path)

raw = extract_text_from_pdf(pdf_path)
print("Extracted PDF.")

structured = structure_medical_report(raw)
print("Structured.")

agents = {
    "Cardiologist": Cardiologist(structured),
    "Psychologist": Psychologist(structured),
    "Pulmonologist": Pulmonologist(structured)
}

responses = {}
with ThreadPoolExecutor() as ex:
    futures = {ex.submit(a.run): role for role, a in agents.items()}
    for fut in as_completed(futures):
        r = fut.result()
        responses[futures[fut]] = r

team = MultidisciplinaryTeam(
    responses["Cardiologist"], responses["Psychologist"], responses["Pulmonologist"]
)
final = team.run()

os.makedirs("results", exist_ok=True)
txt_path = "results/final_diagnosis.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(final)

pdf_path_out = "results/Final_Medical_Report.pdf"
generate_report_pdf(pdf_path_out, structured, responses, final)

print(f"Saved: {txt_path}")
print(f"Saved PDF: {pdf_path_out}")
