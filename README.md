# DentalBot AI — Backend

Backend em Django para o SaaS DentalBot-AI:
• Chatbot WhatsApp para clínicas odontológicas
• Painel com dashboard, conversas e configurações
• Integração com WPPConnect
• Módulo de clientes, planos e trial automático

## Tecnologias
- Python 3.11+
- Django 5+
- PostgreSQL
- Bootstrap 5 (tema CoderTec)
- Webhooks WPPConnect

## Como rodar localmente
git clone https://github.com/seuusuario/backend-dentalbot-ai.git
cd backend-dentalbot-ai

python -m venv venv
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
