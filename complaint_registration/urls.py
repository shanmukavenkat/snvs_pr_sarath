from django.urls import path
from complaint_registration import views

urlpatterns = [
    path('register_complaint/', views.register_complaint)
]