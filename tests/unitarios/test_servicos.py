# -*- coding: utf-8 -*-
import unittest

import mock

from pagador_deposito import servicos


class EntregandoPagamento(unittest.TestCase):
    def test_entrega_tem_malote(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.tem_malote.should.be.truthy

    def test_resultado_eh_malote_como_dict(self):
        entrega = servicos.EntregaPagamento(234)
        entrega.malote = mock.MagicMock()
        entrega.malote.to_dict.return_value = 'MALOTE'
        entrega.processa_dados_pagamento()
        entrega.resultado.should.be.equal({'dados': 'MALOTE'})
