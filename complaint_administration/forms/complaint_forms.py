from django import forms


class complaintRegistrationForm(forms.Form):
    complaint_title = forms.CharField(min_length=20, max_length=100)
    complaint_message = forms.CharField(max_length=1000)
    CHOICES = (
        ('public', 'Public'),
        ('sensitive', 'Sensitive')
    )
    type_of_complaint = forms.ChoiceField(choices=CHOICES)
