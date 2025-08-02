from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import UserProfile


class SignupForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ["username", "password", "email", "realname", "birthday", "phone"]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Username", "required": True}
            ),
            "password": forms.PasswordInput(
                attrs={"placeholder": "Password", "required": True}
            ),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "required": True}),
            "realname": forms.TextInput(attrs={"placeholder": "Real Name"}),
            "birthday": forms.DateInput(attrs={"placeholder": "Birthday", "type": "date"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone Number"}),
        }

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if UserProfile.objects.filter(username=username).exists():
            self.add_error("username", "Username already exists.")
        if UserProfile.objects.filter(email=email).exists():
            self.add_error("email", "Email is already in use. Take another one.")

        return cleaned_data
