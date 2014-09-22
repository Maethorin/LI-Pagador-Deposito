# -*- coding: utf-8 -*-
import json
from urllib import urlencode
from datetime import timedelta, datetime

import requests
from pagador.seguranca import autenticador
from pagador.seguranca.autenticador import TipoAutenticacao
from pagador.seguranca.instalacao import Parametros, InstalacaoNaoFinalizada
from pagador.settings import MERCADOPAGO_REDIRECT_URL
import pagador_mercadopago


class ParametrosPayPal(Parametros):
    @property
    def chaves(self):
        return ["username", "password", "signature", "button_source"]


class TipoToken(object):
    authorization_code = "authorization_code"
    refresh_token = "refresh_token"


class Credenciador(autenticador.Credenciador):
    def __init__(self, configuracao):
        self.conta_id = configuracao.conta_id
        self.usuario = getattr(configuracao, "usuario", "")
        self.tipo = TipoAutenticacao.query_string

    @property
    def chave(self):
        return "SUBJECT"

    def obter_credenciais(self):
        return self.usuario

    def esta_valido(self):
        return True
