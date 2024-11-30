from django.core.exceptions import ValidationError

import requests
import json


def vin_decoder(vin: str) -> str or int:

    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long.")

    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json'
    response = requests.get(url=url)

    if response.status_code == 200:
        vehicle = response.json()
        make = vehicle["Results"][0]["Make"]
        model = vehicle["Results"][0]["Model"]
        year = vehicle["Results"][0]["ModelYear"]
        engine_manufacturer = vehicle["Results"][0]["EngineManufacturer"]
        engine_model = vehicle["Results"][0]["EngineModel"]

        return f"{make} {model} {year} {engine_manufacturer} {engine_model}"
    else:
        return response.status_code
