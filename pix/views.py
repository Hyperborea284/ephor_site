import requests
from django.conf import settings
from django.http import HttpResponse

def criar_pagamento(request):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        descricao = request.POST.get('descricao')
        url_cobranca = 'https://api-pix-h.homolog.pix.ebanx.com.br/v2/cob'

        headers = {
            'Authorization': f'Bearer {settings.CHAVE_PIX}',
            'Content-Type': 'application/json',
            'X-Idempotency-Key': 'IDEM_123456'
        }

        data = {
            'calendario': {
                'expiracao': 3600
            },
            'devedor': {
                'cpf': '12345678909',
                'nome': 'Fulano de Tal'
            },
            'valor': {
                'original': valor
            },
            'chave': settings.CHAVE_PIX,
            'solicitacaoPagador': descricao
        }

        response = requests.post(url_cobranca, headers=headers, json=data)
        resposta_json = response.json()

        if response.status_code == 201:
            qr_code = resposta_json['loc']['qrCode']
            return HttpResponse(qr_code)
        else:
            return HttpResponse(resposta_json['mensagem'], status=response.status_code)

    return HttpResponse('Método não permitido', status=405)
