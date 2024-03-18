from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Complaint
from complaint_registration.forms.complaint_forms import complaintRegistrationForm
from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector, SearchHeadline


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
        return render(request, 'complaint_registration/complaint_registration.html', {'form': form})


def view_complaints(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('Please Login before viewing the complaints')

    # Fetching all complaints from the database
    complaints: Complaint = Complaint.objects.all().order_by('-complaint_time', '-complaint_date')[:100]

    # Filtering complaint that are accessible to the user
    accessible_complaints = list()
    for complaint in complaints:
        if complaint.user == request.user or complaint.type_of_complaint == 'public':
            accessible_complaints.append(complaint)

    return render(request, 'complaint_registration/view_complaints.html', {'complaints': accessible_complaints})


def share_complaint(request):
    pass


def search(request):
    query = request.GET.get('query', '')
    vector = SearchVector('complaint_title', 'complaint_message', 'user__username', 'status',
                          'complaint_time', 'complaint_date')
    results = Complaint.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
    for complaint in results:
        if complaint.rank > 0.001:
            print(complaint.user.username)
    return render(request, 'complaint_registration/view_complaints.html', {'complaints': results})
