from django import forms


class studentRegistrationForm(forms.Form):
    roll_no = forms.CharField(label='Roll No', max_length=10, min_length=10, required=True)
    username = forms.CharField(label='Username', max_length=100, required=True)
    branch = forms.CharField(label='Branch', min_length=6, required=True)
    year = forms.IntegerField(label='Year', min_value=1, max_value=4, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    image = forms.FileField(label='Profile Image', required=False)


class studentLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
