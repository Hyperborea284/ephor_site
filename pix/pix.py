import json
import requests
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from django.conf import settings


class PixAPI:
    def __init__(self):
        self.url_base = settings.PIX_URL_BASE
        self.chave = settings.PIX_CHAVE
        self.chave_privada = settings.PIX_CHAVE_PRIVADA

    def gerar_cobranca(self, valor, descricao):
        endpoint = '/v2/cob'

        headers = {
            'Authorization': f'Bearer {self.chave}',
            'Content-Type': 'application/json',
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
            'chave': self.chave,
            'solicitacaoPagador': descricao
        }

        response = self._enviar_requisicao('post', endpoint, headers, data)

        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(response.json()['mensagem'])

    def _enviar_requisicao(self, metodo, endpoint, headers=None, data=None):
        url = self.url_base + endpoint

        if headers is None:
            headers = {}

        if data is None:
            data = {}

        payload = json.dumps(data).encode('utf-8')
        hash = SHA256.new(payload)

        headers['Content-Length'] = str(len(payload))
        headers['X-Idempotency-Key'] = hash.hexdigest()

        signer = pkcs1_15.new(self._decode_chave_privada())
        signature = signer.sign(hash)

        headers['Authorization'] = f'Bearer {self.chave}.{b64encode(signature).decode()}'

        if metodo.lower() == 'get':
            response = requests.get(url, headers=headers)
        elif metodo.lower() == 'post':
            response = requests.post(url, headers=headers, json=data)
        elif metodo.lower() == 'put':
            response =
