# -*- coding: utf-8 -*-

from pagador.reloaded import entidades
from pagador_deposito.reloaded import cadastro


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'email_comprovante', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total']
    _codigo_gateway = 7

    def __init__(self, loja_id):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id)
        self.preencher_do_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioDeposito()
