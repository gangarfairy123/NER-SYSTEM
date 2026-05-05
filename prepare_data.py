import re

TRAIN_DATA = []

with open("dataset/raw_data.csv", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    text = line.strip()
    entities = []

    # ---------------- SYMPTOMS ----------------
    symptoms_match = re.search(r"Patient presents with (.*?);", text)
    if symptoms_match:
        symptoms = re.split(r" and |,", symptoms_match.group(1))
        for symptom in symptoms:
            symptom = symptom.strip()
            for match in re.finditer(re.escape(symptom), text):
                entities.append((match.start(), match.end(), "SYMPTOM"))

    # ---------------- DISEASE ----------------
    disease_match = re.search(r"diagnosed with (.*?);", text)
    if disease_match:
        disease = disease_match.group(1).strip()
        for match in re.finditer(re.escape(disease), text):
            entities.append((match.start(), match.end(), "DISEASE"))

    # ---------------- DRUG + DOSAGE ----------------
    drug_dose_match = re.search(r"prescribed (\w+) (\d+mg)", text)
    if drug_dose_match:
        drug = drug_dose_match.group(1)
        dose = drug_dose_match.group(2)

        for match in re.finditer(re.escape(drug), text):
            entities.append((match.start(), match.end(), "DRUG"))

        for match in re.finditer(re.escape(dose), text):
            entities.append((match.start(), match.end(), "DOSAGE"))

    # ---------------- FREQUENCY ----------------
    freq_patterns = [
        "once daily", "twice daily", "three times a day",
        "as needed", "at bedtime", "before meals"
    ]

    for pattern in freq_patterns:
        for match in re.finditer(pattern, text):
            entities.append((match.start(), match.end(), "FREQUENCY"))

    for match in re.finditer(r"every \d+ hours", text):
        entities.append((match.start(), match.end(), "FREQUENCY"))

    # ---------------- DURATION ----------------
    for match in re.finditer(r"for \d+ days|for \d+ weeks|for one month", text):
        entities.append((match.start(), match.end(), "DURATION"))

    # Only add if entities exist
    if entities:
        TRAIN_DATA.append((text, {"entities": entities}))

# Debug sample
print("Sample TRAIN_DATA:")
print(TRAIN_DATA[0])