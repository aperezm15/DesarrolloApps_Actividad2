import os

import requests

from app.domain.exceptions import ErrorEnvioCorreo
from app.domain.ports.email_sender import EmailSender

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoEmailSender(EmailSender):
    """Adaptador de salida: envía correos mediante la API HTTPS de Brevo."""

    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")
        self.remitente = os.getenv("EMAIL_REMITENTE")
        self.nombre = os.getenv("EMAIL_NOMBRE_REMITENTE", "API Carreras")

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        cabeceras = {
            "api-key": self.api_key,
            "accept": "application/json",
            "content-type": "application/json",
        }
        datos = {
            "sender": {"name": self.nombre, "email": self.remitente},
            "to": [{"email": destinatario}],
            "subject": asunto,
            "textContent": cuerpo,
        }
        try:
            respuesta = requests.post(BREVO_URL, headers=cabeceras, json=datos, timeout=15)
            respuesta.raise_for_status()
        except requests.RequestException as e:
            detalle = getattr(getattr(e, "response", None), "text", "") or str(e)
            raise ErrorEnvioCorreo(detalle)