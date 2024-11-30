from django.contrib.auth.models import User
from django.db import models

from datetime import date, timedelta

from django.db.models import Prefetch


def get_app_logo(instance, filename) -> str:
    name, extension = filename.split(".")
    return f"static/images/app_logos/{instance.first_name}{instance.last_name}.{extension}"


class Skyonics(models.Model):
    name = models.CharField(max_length=32)
    is_visible = models.BooleanField(default=True)

    @staticmethod
    def get():
        return Skyonics.objects.values()

    @staticmethod
    def get_visible():
        return Skyonics.objects.filter(is_visible=True).values()

    @staticmethod
    def get_skyonics_by_id(skyonics_id: int):
        return Skyonics.objects.filter(id=skyonics_id).values().first()

    def add(self):
        pass

    def __str__(self) -> str:
        return f"{self.name}"


class Applications(models.Model):
    name = models.CharField(max_length=32)
    logo = models.FileField(
        default=None,
        upload_to=get_app_logo,
        blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    @staticmethod
    def get():
        return Applications.objects.values()

    @staticmethod
    def get_visible():
        return Applications.objects.filter(is_visible=True).values()

    @staticmethod
    def get_application_by_id(app_id: int):
        return Applications.objects.filter(id=app_id).values().first()

    def add(self):
        pass

    def __str__(self) -> str:
        return f"{self.name}"


class EldCommands(models.Model):
    command = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)

    @staticmethod
    def get():
        return EldCommands.objects.values()

    @staticmethod
    def get_visible():
        return EldCommands.objects.filter(is_visible=True).values()

    @staticmethod
    def get_command_by_id(command_id: int):
        return EldCommands.objects.filter(id=command_id).values().first()

    def add(self):
        pass

    def __str__(self) -> str:
        return f"{self.command}"


class EldCommandsHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    command_id = models.ForeignKey(EldCommands, on_delete=models.PROTECT)
    skyonics_id = models.ForeignKey(Skyonics, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get():
        return EldCommandsHistory.objects.values()

    @staticmethod
    def get_user_history(user_id: int):
        return (EldCommandsHistory
                .objects
                .select_related("skyonics_id", "command_id")
                .filter(user_id=user_id)
                .order_by("-created_at")
                .all()[:10])

    @staticmethod
    def add(user_id: int, command_id: int, skyonics_id: int, serial_number: str) -> None:
        EldCommandsHistory(
            user_id=user_id,
            command_id=command_id,
            skyonics_id=skyonics_id,
            serial_number=serial_number).save()

    def __str__(self) -> str:
        return f"{self.serial_number} - {self.created_at}"


class MalfunctionLettersHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    application_id = models.ForeignKey(Applications, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=64)
    vehicle_name = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=16)
    driver_name = models.CharField(max_length=64)
    codriver_name = models.CharField(max_length=64, default=None, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField(default=(date.today() + timedelta(days=8)))

    @staticmethod
    def get():
        return (MalfunctionLettersHistory
                .objects
                .select_related("application_id")
                .order_by("expires_at")
                .all()[:10])

    @staticmethod
    def add(user_id: int, application_id: int, company_name: str, vehicle_name: str,
            serial_number: str, driver_name: str, codriver_name: str) -> None:
        MalfunctionLettersHistory(
            user_id=user_id,
            application_id=application_id,
            company_name=company_name,
            vehicle_name=vehicle_name,
            serial_number=serial_number,
            driver_name=driver_name,
            codriver_name=codriver_name
        ).save()

    def __str__(self) -> str:
        return f"{self.company_name} - {self.vehicle_name} - {self.created_at}"
