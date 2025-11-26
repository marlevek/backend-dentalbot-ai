import requests
import base64
from .models import BotConfig
from accounts.models import Client


class WPPConnectAPI:

    def __init__(self, client: Client):
        self.client = client
        self.config, _ = BotConfig.objects.get_or_create(client=client)

        # Exemplo: http://localhost:21465 (instância WPPConnect)
        self.base_url = self.config.instance_url

    # ---------------------------------------
    # Obter QR Code da sessão
    # ---------------------------------------
    def get_qr_code(self):
        try:
            url = f"{self.base_url}/api/{self.config.session_name}/status-session"
            response = requests.get(url).json()

            if response.get("status") == "qrCode":
                qr = response.get("qrcode")
                self.config.qr_code = qr
                self.config.status = "offline"
                self.config.save()
                return qr

            elif response.get("status") == "isLogged":
                self.config.status = "online"
                self.config.qr_code = None
                self.config.save()
                return None

        except Exception as e:
            self.config.status = "offline"
            self.config.save()
            return None

    # ---------------------------------------
    # Verifica status atual do BOT
    # ---------------------------------------
    def get_status(self):
        try:
            url = f"{self.base_url}/api/{self.config.session_name}/status-session"
            response = requests.get(url).json()

            if response.get("status") == "isLogged":
                self.config.status = "online"
            else:
                self.config.status = "offline"

            self.config.save()
            return self.config.status

        except:
            self.config.status = "offline"
            self.config.save()
            return "offline"

    # ---------------------------------------
    # Enviar mensagem pelo WhatsApp
    # ---------------------------------------
    def send_message(self, phone, text):
        try:
            endpoint = f"{self.base_url}/api/{self.config.session_name}/send-text"
            payload = {
                "phone": phone,
                "message": text
            }
            requests.post(endpoint, json=payload)
            return True
        except:
            return False
