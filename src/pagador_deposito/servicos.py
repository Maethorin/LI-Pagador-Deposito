# -*- coding: utf-8 -*-
from pagador import servicos


class EntregaPagamento(servicos.EntregaPagamento):
    def __init__(self, loja_id, plano_indice=1, dados=None):
        super(EntregaPagamento, self).__init__(loja_id, plano_indice, dados=dados)
        self.tem_malote = True

    def processa_dados_pagamento(self):
        self.dados_enviados = self.malote.to_dict()
        self.resultado = {'dados': self.dados_enviados}
