from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import department, Doctor
from .models import booking as Booking

from .forms import (
    bookingform,
    contactform,
    CustomUserCreationForm
)

from .recommendation import recommend_doctors
@login_required
def index(request):
    # person={'name':'vishnu','age':20,'place':'ernakulam'}
    # numbers={'num':[1,2,3,4,5,6,7,8,9,10]}
    return render(request, 'index.html',)
def about(request):
    # fruits = {
    about = {
    #     'fruits': ['apple', 'banana', 'grapes', 'mango']
    }
    return render(request, 'about.html',)
# about={'name':'apolo','year':1983,'place':'chennai'}
def doctors(request):
   dic_doctors={
       "doc":Doctor.objects.all()
    }
   return render(request,'doctors.html',dic_doctors)
def Contact(request):
   if request.method=="POST":
       form=contactform(request.POST)
       if form.is_valid():
           form.save()
           return redirect("index")
   else:
          form=contactform()
   return render(request,"contact.html",{"form":form})
   
def departments(request):
   dic_dept={
   "dept":department.objects.all()
   }
   return render(request,'department.html',dic_dept)


@login_required
def booking(request):
    if request.method == "POST":
        form = bookingform(request.POST, user=request.user)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient_name = request.user.username
            appointment.patient_email = request.user.email
            appointment.save()

            return redirect("patient_dashboard")
    else:
        form = bookingform(user=request.user)

    return render(request, "booking.html", {"form": form})

@login_required
def patient_dashboard(request):

    # Get logged-in patient's email
    patient_email = request.user.email

    # Get patient's appointments
    bookings = Booking.objects.filter(
        patient_email=patient_email
    ).order_by('-booking_on')

    # Get today's date
    today = timezone.localdate()

    # Upcoming appointments
    upcoming_bookings = bookings.filter(
        booking_on__gte=today
    )

    # Previous appointments
    past_bookings = bookings.filter(
        booking_on__lt=today
    )

    # Dashboard information
    context = {
        'bookings': bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'total_bookings': bookings.count(),
        'upcoming_count': upcoming_bookings.count(),
        'past_count': past_bookings.count(),
    }

    return render(request, 'patient_dashboard.html', context)

def signup(request):

    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})
def smart_recommendation(request):
    doctors = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        searched = True

        if symptoms:
            doctors = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recommendation.html",
        {
            "doctors": doctors,
            "symptoms": symptoms,
            "searched": searched,
        },
    )         

    

    

# Create your views here.
