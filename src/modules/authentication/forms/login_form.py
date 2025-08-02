from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username or not password:
            raise forms.ValidationError("Username and password are required.")

        return cleaned_data
