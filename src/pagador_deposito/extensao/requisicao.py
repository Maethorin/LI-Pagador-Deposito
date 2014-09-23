# -*- coding: utf-8 -*-

import urllib

from pagador import settings
from pagador.envio.requisicao import Enviar
from pagador.retorno.models import SituacaoPedido


class EnviarPedido(Enviar):
    def __init__(self, pedido, dados):
        self.pedido = pedido
        self.dados = {}
        self.processa_resposta = True
        self.url = None
        self.grava_identificador = False

    def obter_situacao_do_pedido(self, status_requisicao):
        return SituacaoPedido.SITUACAO_AGUARDANDO_PAGTO

    def processar_resposta(self, resposta):
        return {"content": "OK", "status": 200, "reenviar": False}
