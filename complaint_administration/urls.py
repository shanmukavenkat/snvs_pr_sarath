from django.urls import path
from complaint_administration import views

urlpatterns = [
    path('register_complaint/', views.register_complaint),
    path('view_complaints/', views.view_complaints),
    path('search_complaints/', views.search),
    path('view_complaint/<slug:complaint_id>/', views.view_complaint, name='view_complaint'),
    path('escalate_complaint/<slug:complaint_id>/', views.escalate_complaint, name='escalate_complaint')
]