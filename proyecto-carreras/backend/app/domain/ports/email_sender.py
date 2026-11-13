from abc import ABC, abstractmethod


class EmailSender(ABC):
    """Puerto de salida: enviar correos electrónicos."""

    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None: ...