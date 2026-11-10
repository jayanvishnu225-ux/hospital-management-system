from django.db import models
from django.conf import settings

# Create your models here.
class department(models.Model):
    department_name=models.CharField(max_length=100)
    department_disc=models.TextField()
    def __str__(self):
        return self.department_name

class  Doctor(models.Model):
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='doctor_profile'
)
    doc_name=models.CharField(max_length=100)
    doc_disc=models.TextField()
    doc_spec=models.CharField(max_length=100)
    doc_dept=models.ForeignKey(department,on_delete=models.CASCADE)
    doc_image=models.ImageField(upload_to='doctors/',null=True,blank=True)
    
    
    def __str__(self):
        return self.doc_name
class booking(models.Model):
       STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
       patient_name=models.CharField(max_length=100)
       patient_email=models.EmailField()
       patient_phone=models.CharField(max_length=15)
       booking_on=models.DateField()
       doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
       status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
       def __str__(self):
        return (f"{self.patient_name} - {self.doctor.doc_name}")
class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    Address=models.TextField()
    def __str__(self):
        return self.name
