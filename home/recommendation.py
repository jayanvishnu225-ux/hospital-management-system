from home.models import Doctor


SYMPTOM_RULES = {
    "chest pain": ["Cardiologist", "Heart Specialist"],
    "heart problem": ["Cardiologist", "Heart Specialist"],
    "skin rash": ["Dermatologist", "Skin Specialist"],
    "itching": ["Dermatologist", "Skin Specialist"],
    "headache": ["Neurologist", "Brain Specialist", "Nuro"],
    "migraine": ["Neurologist", "Brain Specialist", "Nuro"],
    "bone pain": [
        "Orthopedic Surgeon",
        "Orthopedic Specialist",
        "Bone Specialist",
    ],
    "joint pain": [
        "Orthopedic Surgeon",
        "Orthopedic Specialist",
        "Bone Specialist",
    ],
    "child fever": ["Pediatrician", "Child Specialist"],
    "ear pain": ["ENT Specialist", "ENT Surgeon"],
    "sore throat": ["ENT Specialist", "ENT Surgeon"],
    "eye pain": ["Ophthalmologist", "Eye Specialist"],
    "blurred vision": ["Ophthalmologist", "Eye Specialist"],
    "fever": ["General Physician", "Internal Medicine"],
    "cough": ["General Physician", "Internal Medicine"],
}



def find_specializations(symptoms):
    symptoms = symptoms.lower().strip()
    matched_specializations = set()

    for symptom, specializations in SYMPTOM_RULES.items():
        if symptom in symptoms:
            matched_specializations.update(specializations)

    return sorted(matched_specializations)


def recommend_doctors(symptoms):
    specializations = find_specializations(symptoms)

    if not specializations:
        return Doctor.objects.none()

    return Doctor.objects.filter(
        doc_spec__in=specializations
    ).select_related("doc_dept").distinct()