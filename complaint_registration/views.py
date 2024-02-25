from django.http import HttpResponse
from django.shortcuts import render
from .models import Complaint
from complaint_registration.forms.complaint_forms import complaintRegistrationForm


def register_complaint(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Please Login before filing a complaint")

        form = complaintRegistrationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Please Enter correct details")

        Complaint.objects.create(user=user, **form.cleaned_data)
        return HttpResponse('Complaint has been successfully registered')

    else:
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Please login")
        form = complaintRegistrationForm()
        return render(request, 'complaint_registration.html', {'form': form})
