from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Create your forms here.


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your first name"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your last name"}
        )
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Re-enter your password"}
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your password"}
        )
