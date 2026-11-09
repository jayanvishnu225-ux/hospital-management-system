from django.contrib import admin
from .models import contact, department
from .models import booking
from .models import Doctor
admin.site.register(department)
admin.site.register(Doctor)
admin.site.register(booking)
admin.site.register(contact)
# Register your models here.
