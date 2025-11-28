import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

WHATSAPP_TOKEN = "SEU_TOKEN_AQUI"
WHATSAPP_PHONE_ID = "SEU_PHONE_NUMBER_ID_AQUI"

@csrf_exempt
def test_message(request):
    phone = request.GET.get("phone")

    if not phone:
        return JsonResponse({"error": "Informe o número no formato 55DDDNUMERO (?phone=...)"}, status=400)

    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": { "body": "Mensagem de teste enviada pelo app Dentalbot-AI para validação da Meta. ✔️" }
    }

    response = requests.post(url, json=payload, headers=headers)

    return JsonResponse({
        "status": "enviado",
        "meta_response": response.json()
    })
