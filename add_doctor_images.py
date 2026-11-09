import urllib.request
from pathlib import Path

from django.conf import settings
from home.models import Doctor

# Fictional profile portraits are selected using the doctors' names.
GENDER_BY_DOCTOR_NAME = {
    "arun menon": "men",
    "meera nair": "women",
    "rahul das": "men",
    "anjali raj": "women",
    "neha thomas": "women",
    "vivek kumar": "men",
    "akhil varma": "men",
    "divya mohan": "women",
    "sanjay rao": "men",
    "nikhil suresh": "men",
    "kavya pillai": "women",
    "manu joseph": "men",
    "priya krishnan": "women",
    "rohan mathew": "men",
    "sneha paul": "women",
    "anoop babu": "men",
    "lakshmi devi": "women",
    "kiran george": "men",
    "amal james": "men",
    "riya bose": "women",
    "deepak lal": "men",
    "sreeram krish": "men",
    "fathima salim": "women",
    "joseph antony": "men",
}

# Save images inside media/doctors/
BASE_DIR = Path(settings.BASE_DIR)
MEDIA_ROOT = Path(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else BASE_DIR / "media"

image_folder = MEDIA_ROOT / "doctors"
image_folder.mkdir(parents=True, exist_ok=True)

doctors = Doctor.objects.order_by("id")
updated = 0
failed = 0

for doctor in doctors:
    # Keep the two images that were uploaded manually.
    if doctor.id in {1, 2} and doctor.doc_image:
        print(f"Preserving uploaded image: {doctor.doc_name}")
        continue

    gender = GENDER_BY_DOCTOR_NAME.get(doctor.doc_name.strip().casefold())
    if gender is None:
        failed += 1
        print(f"Failed: no gender mapping for {doctor.doc_name}")
        continue

    photo_id = ((doctor.id - 1) % 99) + 1
    image_name = f"doctor_{doctor.id}_{gender}.jpg"
    image_path = image_folder / image_name

    if doctor.doc_image.name == f"doctors/{image_name}" and image_path.is_file():
        print(f"Already has matching image: {doctor.doc_name}")
        continue

    url = f"https://randomuser.me/api/portraits/{gender}/{photo_id}.jpg"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ClinicDemo/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            image_data = response.read()

        # Check that the response resembles a JPEG file
        if not image_data.startswith(b"\xff\xd8\xff"):
            raise ValueError("Downloaded file is not a JPEG image")

        image_path.write_bytes(image_data)

        # Store a path relative to MEDIA_ROOT
        doctor.doc_image = f"doctors/{image_name}"
        doctor.save(update_fields=["doc_image"])

        updated += 1
        print(f"Added image: {doctor.doc_name}")

    except Exception as error:
        failed += 1
        print(f"Failed: {doctor.doc_name}: {error}")

print("\nImage assignment completed.")
print("New images:", updated)
print("Failed:", failed)
print(
    "Doctors with images:",
    Doctor.objects.exclude(doc_image="").exclude(doc_image__isnull=True).count(),
)
print("Image folder:", image_folder)