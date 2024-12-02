from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from django.apps import apps

from django.core.exceptions import ValidationError

from django.http import FileResponse

from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm, VinDecoderForm, EldFixerForm, MalfunctionLetterForm

from utils.vin_decoder import vin_decoder
from utils.skyonics_commands import send_command
from utils.malfunction_letters import generate_malfunction_letter

from datetime import datetime, timedelta


def log_in(request) -> render:
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get("username").lower()
            password = login_form.cleaned_data.get("password")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.warning(request=request, message="User does not exits.")
                return redirect(to="login")

            user = authenticate(username=username, password=password)

            if not user:
                messages.warning(request=request, message="Incorrect username or password.")
                return redirect(to="login")

            login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(to="fixer")
    else:
        login_form = LoginForm()

        return render(
            request=request,
            template_name="auth/login.html",
            context={
                "title": "Login",
                "form": login_form
            }

        )


def log_out(request) -> redirect:
    logout(request=request)
    return redirect(to="login")


def register(request) -> render:
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                form.clean_username()
                form.clean_password2()
                form.save()

                messages.success(request=request, message="User successfully created!")
                return redirect(to="login")
            except ValidationError:
                messages.warning(request=request, message="Form is not valid!")
            except Exception as e:
                messages.error(request=request, message=f"{e.__class__}")
        else:
            messages.warning(request=request, message="Form is not valid!")
            return redirect(to="register")
    else:
        register_form = RegisterForm()

        return render(
            request=request,
            template_name="auth/register.html",
            context={
                "title": "Register",
                "form": register_form
            }
        )


def fixer_redirect(request) -> redirect:
    return redirect(to="fixer")


def fixer(request) -> render or redirect:
    if not request.user.is_authenticated:
        return redirect(to="login")

    skyonics_model = apps.get_model("app", "Skyonics")
    eldcommands_model = apps.get_model("app", "EldCommands")
    eldcommandshistory_model = apps.get_model("app", "EldCommandsHistory")

    vin_form = VinDecoderForm()
    fixer_form = EldFixerForm()

    decoded_vin = None
    command_response = None

    user = User.objects.filter(username=request.user).values().first()
    user_id = user.get("id")

    if request.method == "POST":
        if request.POST.get("vin_submit"):
            vin_form = VinDecoderForm(request.POST)
            if vin_form.is_valid():
                try:
                    vin = vin_form.cleaned_data.get("vin")
                    decoded_vin = vin_decoder(vin=vin)
                except ValidationError as e:
                    messages.warning(request=request, message=e.message)

        elif request.POST.get("fixer_submit"):
            fixer_form = EldFixerForm(request.POST)
            if fixer_form.is_valid():
                eld_sn = fixer_form.cleaned_data.get("eld_sn")
                command_id = fixer_form.cleaned_data.get("command")
                skyonics_id = fixer_form.cleaned_data.get("skyonics")
                try:
                    command = eldcommands_model.get_command_by_id(command_id=command_id).get("command")
                    skyonics = skyonics_model.get_skyonics_by_id(skyonics_id=skyonics_id).get("name")

                    response = send_command(eld_sn=eld_sn, command=command, skyonics=skyonics)

                    command_response = {
                        "response": response,
                        "eld_sn": eld_sn,
                        "command": command,
                        "eta": (datetime.now() + timedelta(minutes=2)).time().strftime("%I:%M:%S %p")
                    }

                    if response == 200:
                        eldcommandshistory_model.add(
                            user_id=request.user,
                            command_id=eldcommands_model.objects.get(id=command_id),
                            skyonics_id=skyonics_model.objects.get(id=skyonics_id),
                            serial_number=eld_sn)

                except ValidationError as e:
                    messages.warning(request=request, message=e.message)

    command_history = eldcommandshistory_model.get_user_history(user_id=user_id)

    return render(
        request=request,
        template_name="fixer.html",
        context={
            "title": "Fixer",
            "vin_form": vin_form,
            "fixer_form": fixer_form,
            "decoded_vin": decoded_vin,
            "command_response": command_response,
            "command_history": command_history})


def malfunctionletters(request) -> render or FileResponse:
    if not request.user.is_authenticated:
        return redirect(to="login")

    applications_model = apps.get_model("app", "Applications")
    malfunctionlettershistory_model = apps.get_model("app", "MalfunctionLettersHistory")

    if request.method == "POST":
        form = MalfunctionLetterForm(request.POST)
        if form.is_valid():
            form_dict: dict = form.cleaned_data
            buffer, file_name = generate_malfunction_letter(letter_data=form_dict)

            malfunctionlettershistory_model.add(
                user_id=request.user,
                application_id=applications_model.objects.get(id=form_dict.get("application")),
                company_name=form_dict.get("company_name"),
                vehicle_name=form_dict.get("vehicle"),
                serial_number=form_dict.get("eld_sn"),
                driver_name=form_dict.get("driver_name"),
                codriver_name=form_dict.get("codriver_name"),
                expires_at=(datetime.now() + timedelta(days=8)).date())

            return FileResponse(buffer, as_attachment=True, filename=file_name)
    else:
        form = MalfunctionLetterForm()

    malfunction_letter_history = malfunctionlettershistory_model.get()

    return render(
        request=request,
        template_name="malfunctionletters.html",
        context={
            "title": "Malfunction Letters",
            "ml_form": form,
            "malfunction_letter_history": malfunction_letter_history})
