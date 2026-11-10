
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('doctors/', views.doctors, name='doctors'),
    path('departments/', views.departments, name='departments'),
    path('booking/', views.booking, name='booking'),
    path(
        'patient_dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('smart_recommendation/', views.smart_recommendation, name='smart_recommendation'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),

path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

path(
    'update_appointment/<int:appointment_id>/',
    views.update_appointment_status,
    name='update_appointment_status'
),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
