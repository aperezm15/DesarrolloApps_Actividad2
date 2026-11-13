from app.domain.ports.email_sender import EmailSender


class ConsoleEmailSender(EmailSender):
    """Adaptador para desarrollo: imprime el correo en la terminal."""

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        print("\n===== CORREO SIMULADO =====")
        print(f"Para:   {destinatario}")
        print(f"Asunto: {asunto}")
        print(cuerpo)
        print("===========================\n")