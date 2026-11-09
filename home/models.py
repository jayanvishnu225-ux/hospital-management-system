from django.db import models

# Create your models here.
class department(models.Model):
    department_name=models.CharField(max_length=100)
    department_disc=models.TextField()
    def __str__(self):
        return self.department_name

class  Doctor(models.Model):
    doc_name=models.CharField(max_length=100)
    doc_disc=models.TextField()
    doc_spec=models.CharField(max_length=100)
    doc_dept=models.ForeignKey(department,on_delete=models.CASCADE)
    doc_image=models.ImageField(upload_to='doctors/',null=True,blank=True)
    def __str__(self):
        return self.doc_name
class booking(models.Model):
    patient_name=models.CharField(max_length=100)
    patient_email=models.EmailField()
    patient_phone=models.CharField(max_length=15)
    booking_on=models.DateField()
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    def __str__(self):
        return (f"{self.patient_name} - {self.doctor.doc_name}")
class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    Address=models.TextField()
    def __str__(self):
        return self.name
