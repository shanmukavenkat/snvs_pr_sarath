from django.http import HttpResponse
from django.shortcuts import render
from user_administration.forms import student_forms
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout


def student_registration(request):
    if request.method == "POST":
        form = student_forms.studentRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # print(form.cleaned_data)
            CustomUser.objects.create_user(**form.cleaned_data)

            return HttpResponse("The data is clean")
        else:
            return HttpResponse("The data is not clean")
    else:
        form = student_forms.studentRegistrationForm()
        return render(request, 'student_registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = student_forms.studentLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return HttpResponse("You are logged In")
            else:
                return HttpResponse("Invalid username or password")

    else:
        form = student_forms.studentLoginForm()
        return render(request, 'user_login.html', {'form': form})
