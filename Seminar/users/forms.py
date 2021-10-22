from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserCreationForm
from users.models import korisnici

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 60, help_text = 'Required. Add valid email address', required=False)

    class Meta:
        model = korisnici
        fields = ('email', 'username')
