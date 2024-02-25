from django.http import HttpResponse
from django.shortcuts import render
from user_registration.forms.student_forms import studentRegistrationForm
from .models import CustomUser


def student_registration(request):
    if request.method == "POST":
        form = studentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            CustomUser.objects.create(**form.cleaned_data)

            return HttpResponse("The data is clean")
        else:
            return HttpResponse("The data is not clean")
    else:
        form = studentRegistrationForm()
        return render(request, 'student_registration.html', {'form': form})
