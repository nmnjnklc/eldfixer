from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter

from django.apps import apps

from datetime import datetime
from pathlib import Path

import io


BASE_DIR = Path(__file__).resolve().parent.parent


def generate_malfunction_letter(letter_data: dict):
    global BASE_DIR

    application_model = apps.get_model("app", "Applications")

    buffer = io.BytesIO()

    app_id = letter_data.get("application")
    company_name = letter_data.get("company_name")
    company_dot = letter_data.get("company_dot_number")
    driver_name = letter_data.get("driver_name")
    codriver_name = letter_data.get("codriver_name")
    vehicle_number = letter_data.get("vehicle")
    safety_contact = letter_data.get("safety_contact")

    app_name = application_model.get_application_by_id(app_id=app_id).get("name")
    logo_path = Path(BASE_DIR, "static", "images", "app_logos", f"{app_name.lower().replace(' ', '')}.png")

    if app_name == "ELD Rider":
        logo = Image(logo_path, width=250, height=60)

    if app_name == "XELD":
        logo = Image(logo_path, width=170, height=60)

    if app_name == "Optima ELD":
        logo = Image(logo_path, width=270, height=60)

    if app_name == "Pro Ride ELD":
        logo = Image(logo_path, width=250, height=60)

    if app_name == "Sparkle ELD":
        logo = Image(logo_path, width=300, height=60)

    if app_name == "Xplore ELD":
        logo = Image(logo_path, width=250, height=60)

    if app_name == "PTI ELD":
        logo = Image(logo_path, width=80, height=60)

    if app_name == "TX ELD":
        logo = Image(logo_path, width=170, height=60)

    if app_name == "EVA ELD":
        logo = Image(logo_path, width=250, height=60)

    if app_name == "RouteMate ELD":
        logo = Image(logo_path, width=300, height=60)

    if app_name == "Apex ELD":
        logo = Image(logo_path, width=80, height=60)

    if app_name == "Rock ELD":
        logo = Image(logo_path, width=250, height=60)

    if app_name == "PEAK ELD":
        logo = Image(logo_path, width=65, height=60)

    if app_name == "POP ELD":
        logo = Image(logo_path, width=150, height=60)

    current_date: str = str(datetime.now().date()).replace("-", "_")

    solo_driver: list[str] = ["Driver", driver_name, vehicle_number, "has", "he is", "his", app_name, "driver is",
                              "he needs", "driver is", "driver is", safety_contact]

    team_drivers: list[str] = ["Drivers", f"{driver_name} and {codriver_name}", vehicle_number, "have", "they are",
                               "their", app_name, "drivers are", "they need", "drivers are",
                               "drivers are", safety_contact]

    text = (
        '&nbsp; &nbsp; {0} {1} from unit {2} {3} reported that {4} experiencing issues with {5} ELD application due '
        'to device defect, issued from {6}.<br /><br />&nbsp; &nbsp; &nbsp; &nbsp; The {7} not receiving proper '
        'information on ELD application due to device defect, hence {8} to replace the device as soon as possible. '
        'In the interim, according to 395.4 "ELD Malfunctions and Data Diagnostics", the {9} authorized to use manual '
        'rods (paper logs). The {10} required to manually prepare a record of duty status in accordance with 395.8 '
        'until the ELD is serviced and brought back into compliance with this subpart.'
        '<br /><br />&nbsp; &nbsp; Should you have any questions or if you require any additional information, '
        'please contact the SAFETY DEPARTMENT at phone number: &nbsp; {11}')

    footer = f"Respectfully, {app_name.upper()} SUPPORT TEAM"

    styles = ParagraphStyle(name='CustomStyle', fontSize=14, fontName='Helvetica', leading=16)
    center_styles = ParagraphStyle(name='CustomStyle', fontSize=14, fontName='Helvetica', alignment=1)
    justify_styles = ParagraphStyle(name='CustomStyle', fontSize=14, fontName='Helvetica', leading=18, alignment=4)
    right_styles = ParagraphStyle(name='CustomStyle', fontSize=14, fontName='Helvetica', leading=16, alignment=2)

    elements = [
        logo, Spacer(1, 32),
        Paragraph("<strong>ELD MALFUNCTION LETTER</strong>", center_styles), Spacer(1, 32),
        Paragraph(f"Company: <strong>{company_name}</strong>", styles), Spacer(1, 8),
        Paragraph(f"DOT number: <strong>{company_dot}</strong>", styles), Spacer(1, 8),
        Paragraph(f"Driver name: <strong>{driver_name}</strong>", styles), Spacer(1, 8)]

    if len(codriver_name) > 0:
        text = text.format(*team_drivers)
        pdf_name: str = f"{driver_name}_{codriver_name}_{current_date}.pdf"
        elements.append(Paragraph(f"Codriver name: <strong>{codriver_name}</strong>", styles))
        elements.append(Spacer(1, 8))
    else:
        text = text.format(*solo_driver)
        pdf_name: str = f"{driver_name}_{current_date}.pdf"

    elements.append(Paragraph(f"Truck number: <strong>{vehicle_number}</strong>", styles))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Date: <strong>{datetime.now().date().strftime('%b %d, %Y')}</strong>", styles))
    elements.append(Spacer(1, 32))
    elements.append(Paragraph(text, justify_styles))
    elements.append(Spacer(1, 32))
    elements.append(Paragraph(footer, right_styles))

    pdf_name = pdf_name.replace(" ", "_")

    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    pdf.build(elements)

    buffer.seek(0)

    return buffer, pdf_name
