from django.apps import apps

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, CharField, TextInput, PasswordInput, ChoiceField

from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    first_name = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name"
            }
        )
    )

    last_name = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name"
            }
        )
    )

    username = CharField(
        label="",
        min_length=4,
        max_length=150,
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        )
    )

    password1 = CharField(
        label="",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )

    password2 = CharField(
        label="",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password confirmation"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data.get("username"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            password=self.cleaned_data.get("password1")
        )
        return user


class LoginForm(Form):
    username = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username"
            }
        )
    )

    password = CharField(
        label="",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )


class VinDecoderForm(Form):
    vin = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Vehicle Identification Number"
            }
        )
    )


class EldFixerForm(Form):
    @staticmethod
    def get_command_choices() -> tuple:
        command_model = apps.get_model("app", "EldCommands")
        return tuple((c.get("id"), c.get("command")) for c in command_model.get_visible())

    @staticmethod
    def get_skyonics_choices() -> tuple:
        skyonics_model = apps.get_model("app", "Skyonics")
        return tuple((s.get("id"), s.get("name")) for s in skyonics_model.get_visible())

    eld_sn = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "ELD serial number"
            }
        )
    )

    command = ChoiceField(choices=get_command_choices())

    skyonics = ChoiceField(choices=get_skyonics_choices())


class MalfunctionLetterForm(Form):
    @staticmethod
    def get_choices() -> tuple:
        apps_model = apps.get_model("app", "Applications")
        return tuple((a.get("id"), a.get("name")) for a in apps_model.get_visible())

    application = ChoiceField(choices=get_choices(), label="")

    company_name = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company name"
            }
        )
    )

    company_dot_number = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company DOT number"
            }
        )
    )

    driver_name = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Driver name"
            }
        )
    )

    codriver_name = CharField(
        label="",
        required=False,
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Codriver name"
            }
        )
    )

    vehicle = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Vehicle number"
            }
        )
    )

    eld_sn = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "ELD serial number"
            }
        )
    )

    safety_contact = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Safety manager contact"
            }
        )
    )
