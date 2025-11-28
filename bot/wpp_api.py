import requests
import base64

class WPPConnectAPI:

    def __init__(self, client):
        """
        Cada cliente tem a sua instância configurada pelo painel.
        """
        self.client = client
        self.base_url = client.instance_url.rstrip("/")  # remove barra final
        self.session = client.session_name or "dentalbot"
        self.token = client.api_key or ""  # se quiser autenticação futura

    # ========================
    # 🔹 Enviar mensagem
    # ========================
    def send_message(self, phone, text):
        url = f"{self.base_url}/api/{self.session}/send-message"

        payload = {
            "phone": phone,
            "message": text
        }

        try:
            r = requests.post(url, json=payload, timeout=10)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    # ========================
    # 🔹 Status da sessão
    # ========================
    def get_status(self):
        url = f"{self.base_url}/api/{self.session}/status-session"
        try:
            r = requests.get(url, timeout=10)
            return r.json()
        except:
            return {"status": "offline"}

    # ========================
    # 🔹 Buscar QR Code
    # ========================
    def get_qr_code(self):
        url = f"{self.base_url}/api/{self.session}/qrcode"

        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            if "qrcode" in data:
                return data["qrcode"]  # já vem em Base64

            return None

        except Exception:
            return None

