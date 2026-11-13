import os

from app.domain.ports.email_sender import EmailSender
from app.infrastructure.email.brevo_email_sender import BrevoEmailSender
from app.infrastructure.email.console_email_sender import ConsoleEmailSender


def get_email_sender() -> EmailSender:
    """Si hay API key usa Brevo; si no, simula el envío por consola."""
    if os.getenv("BREVO_API_KEY") and os.getenv("EMAIL_REMITENTE"):
        return BrevoEmailSender()
    return ConsoleEmailSender()