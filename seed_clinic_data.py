import random
from datetime import date, timedelta

from django.db import transaction
from home.models import department, Doctor,booking


# Reproducible synthetic data
rng = random.Random(42)

departments_data = [
    ("Cardiology", "Heart and cardiovascular care"),
    ("Dermatology", "Skin, hair and nail care"),
    ("Neurology", "Brain and nervous system care"),
    ("Orthopedics", "Bone, joint and muscle care"),
    ("Pediatrics", "Healthcare for children"),
    ("ENT", "Ear, nose and throat care"),
    ("Ophthalmology", "Eye care and vision"),
    ("General Medicine", "General health consultations"),
]

doctors_data = [
    ("Arun Menon", "Cardiologist", "Cardiology"),
    ("Meera Nair", "Cardiologist", "Cardiology"),
    ("Rahul Das", "Heart Specialist", "Cardiology"),

    ("Anjali Raj", "Dermatologist", "Dermatology"),
    ("Neha Thomas", "Skin Specialist", "Dermatology"),
    ("Vivek Kumar", "Dermatologist", "Dermatology"),

    ("Akhil Varma", "Neurologist", "Neurology"),
    ("Divya Mohan", "Neurologist", "Neurology"),
    ("Sanjay Rao", "Brain Specialist", "Neurology"),

    ("Nikhil Suresh", "Orthopedic Surgeon", "Orthopedics"),
    ("Kavya Pillai", "Orthopedic Specialist", "Orthopedics"),
    ("Manu Joseph", "Bone Specialist", "Orthopedics"),

    ("Priya Krishnan", "Pediatrician", "Pediatrics"),
    ("Rohan Mathew", "Child Specialist", "Pediatrics"),
    ("Sneha Paul", "Pediatrician", "Pediatrics"),

    ("Anoop Babu", "ENT Specialist", "ENT"),
    ("Lakshmi Devi", "ENT Surgeon", "ENT"),
    ("Kiran George", "ENT Specialist", "ENT"),

    ("Amal James", "Ophthalmologist", "Ophthalmology"),
    ("Riya Bose", "Eye Specialist", "Ophthalmology"),
    ("Deepak Lal", "Ophthalmologist", "Ophthalmology"),

    ("Sreeram Krish", "General Physician", "General Medicine"),
    ("Fathima Salim", "General Physician", "General Medicine"),
    ("Joseph Antony", "Internal Medicine", "General Medicine"),
]

first_names = [
    "Aarav", "Ananya", "Adithya", "Diya", "Ishan",
    "Maya", "Nikhil", "Priya", "Rahul", "Sneha",
    "Vishnu", "Amala", "Kiran", "Meera", "Rohan",
    "Devika", "Arjun", "Nila", "Manu", "Akhila"
]

last_names = [
    "Nair", "Menon", "Thomas", "Pillai", "Joseph",
    "Kumar", "Varma", "Das", "Rao", "George"
]


@transaction.atomic
def seed_data():
    created_departments = 0
    created_doctors = 0
    created_bookings = 0

    # 1. Create departments
    department_objects = {}

    for name, description in departments_data:
        obj, created = department.objects.get_or_create(
           department_name=name,
            defaults={"department_disc": description}
        )
        department_objects[name] = obj

        if created:
            created_departments += 1

    # 2. Create doctors
    for name, specialization, department_name in doctors_data:
        obj, created = Doctor.objects.get_or_create(
            doc_name=name,
            doc_spec=specialization,
            doc_dept=department_objects[department_name],
            defaults={
                "doc_disc": f"{specialization} providing care in {department_name}."
            },
        )

        if created:
            created_doctors += 1

    # Include existing doctors too
    doctor_objects = list(Doctor.objects.order_by("id"))

    if not doctor_objects:
        print("No doctors available. Cannot create bookings.")
        return

    # 3. Create 200 fictional bookings
    today = date.today()

    for i in range(1, 201):
        patient_name = (
            f"{rng.choice(first_names)} "
            f"{rng.choice(last_names)}"
        )

        # Reserved example.com domain and clearly synthetic phone
        phone = f"000000{i:04d}"
        email = f"patient{i:03d}@example.com"

        doctor = rng.choice(doctor_objects)
        booking_date = today - timedelta(
            days=rng.randint(0, 364)
        )

        _, created = booking.objects.get_or_create(
            patient_name=patient_name,
            patient_phone=phone,
            patient_email=email,
            doctor=doctor,
            booking_on=booking_date
        )

        if created:
            created_bookings += 1

    print("\nSynthetic data generation completed!")
    print("New departments:", created_departments)
    print("New doctors:", created_doctors)
    print("New bookings:", created_bookings)

    print("\nCurrent database totals:")
    print("Departments:", department.objects.count())
    print("Doctors:", Doctor.objects.count())
    print("Bookings:", booking.objects.count())
seed_data()