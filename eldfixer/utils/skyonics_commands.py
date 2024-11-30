from django.core.exceptions import ValidationError

from dotenv import dotenv_values
from pathlib import Path
import requests
import json

BASE_DIR: Path = Path(__file__).resolve().parent.parent
ENV: dict = dotenv_values(
    dotenv_path=Path(BASE_DIR, ".env"))

SKYONICS_BASE_URL: str = ENV.get("skyonics_base_url")
SKYONICS_API_KEYS: dict = json.loads(
    s=ENV.get("skyonics_api_keys"))


def send_command(eld_sn: str, command: str, skyonics: str) -> int:
    global SKYONICS_BASE_URL
    global SKYONICS_API_KEYS

    if len(eld_sn) != 12:
        raise ValidationError("ELD serial number must be exactly 12 characters long.")

    if eld_sn[0:3] not in ["87A", "87B", "87U", "88A", "88B", "88U"]:
        raise ValidationError("Provided ELD is not a Geometris device.")

    api_key: str = SKYONICS_API_KEYS.get(skyonics)

    url: str = f"{SKYONICS_BASE_URL}/api/skyonics/devicecommand?APIKey={api_key}&serialNumber={eld_sn}&mode=0"
    headers: dict = {"Content-Type": "application/json", "Accept": "application/json"}
    request = requests.post(
        url=url,
        data=f'"{command}"',
        headers=headers,
        verify=False)

    return request.status_code
