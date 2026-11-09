from django.test import TestCase
from django.urls import reverse

from .models import Doctor, department
from .recommendation import recommend_doctors


class DoctorsViewTests(TestCase):
    def test_doctors_page_lists_doctors(self):
        dept = department.objects.create(
            department_name='Cardiology',
            department_disc='Heart care',
        )
        Doctor.objects.create(
            doc_name='Dr. Example',
            doc_disc='Experienced physician',
            doc_spec='Cardiology',
            doc_dept=dept,
        )

        response = self.client.get(reverse('doctors'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Example')


class DoctorRecommendationTests(TestCase):
    def test_recommends_doctors_for_matching_symptoms(self):
        dept = department.objects.create(
            department_name='Dermatology',
            department_disc='Skin care',
        )
        doctor = Doctor.objects.create(
            doc_name='Dr. Skin',
            doc_disc='Skin specialist',
            doc_spec='Dermatologist',
            doc_dept=dept,
        )

        recommendations = recommend_doctors('I have a skin rash and itching')

        self.assertIn(doctor, recommendations)
        self.assertEqual(recommendations.get().doc_dept.department_name, 'Dermatology')

    def test_returns_no_doctors_for_unmatched_symptoms(self):
        self.assertFalse(recommend_doctors('unrecognized symptom').exists())

    def test_smart_recommendation_page_displays_matching_doctors(self):
        dept = department.objects.create(
            department_name='Dermatology',
            department_disc='Skin care',
        )
        Doctor.objects.create(
            doc_name='Dr. Skin',
            doc_disc='Skin specialist',
            doc_spec='Dermatologist',
            doc_dept=dept,
        )

        response = self.client.post(
            reverse('smart_recommendation'),
            {'symptoms': 'skin rash'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Skin')
        self.assertContains(response, 'Dermatology')
