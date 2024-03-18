from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from user_administration.escalation_models import EscalationStructure
from complaint_administration.models.complaint_models import Complaint
from complaint_administration.forms.complaint_forms import complaintRegistrationForm
from django.contrib.postgres.search import SearchRank, SearchVector
from django.contrib.contenttypes.models import ContentType


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
        return render(request, 'complaint_administration/complaint_registration.html', {'form': form})


def view_complaints(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('Please Login before viewing the complaints')

    # Fetching all complaints from the database
    complaints: Complaint = Complaint.objects.all().order_by('-complaint_time', '-complaint_date')[:100]

    # Filtering complaint that are accessible to the user
    accessible_complaints = list()
    for complaint in complaints:
        if complaint.user_object == request.user or complaint.type_of_complaint == 'public':
            accessible_complaints.append(complaint)

    return render(request, 'complaint_administration/view_complaints.html', {'complaints': accessible_complaints})


def view_complaint(request, complaint_id):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('Please Login before Viewing a Complaint')
    complaint = Complaint.objects.get(complaint_id=complaint_id)

    return render(request, 'complaint_administration/view_complaint.html', {'complaint': complaint})


def share_complaint(request):
    pass


def search(request):
    query = request.GET.get('query', '')
    vector = SearchVector('complaint_title', 'complaint_message', 'status',
                          'complaint_time', 'complaint_date', 'counsellor_complaints', 'complaint_id')
    results = Complaint.objects.annotate(rank=SearchRank(vector, query)).filter().order_by('-rank')
    return render(request, 'complaint_administration/view_complaints.html', {'complaints': results})


def escalate_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = Complaint.objects.filter(complaint_id=complaint_id)[0]
        user = complaint.user_object
        next_escalation_level = EscalationStructure.objects.filter(id=complaint.escalated_to.id+1)

        if next_escalation_level:
            next_escalation_level = next_escalation_level[0]
            user_args = dict()

            user_args[f'{next_escalation_level.student_relation_identifier}'] = getattr(user, f'{next_escalation_level.student_relation_identifier}_id')
            next_level_authority = apps.get_model(f'user_administration.{next_escalation_level.role}')
            print(next_level_authority)
            next_level_authority_instance = next_level_authority.objects.get(**user_args)
            next_level_authority_content_type = ContentType.objects.get_for_model(next_level_authority_instance)
            complaint.content_type = next_level_authority_content_type
            complaint.object_id = next_level_authority_instance.id
            complaint.escalated_to = next_escalation_level
            complaint.save()
            return HttpResponse('Complaint has been escalated Successfully')
        else:
            return HttpResponse('Complaint cant be escalated further')


def de_escalate_complaint(request):
    pass
