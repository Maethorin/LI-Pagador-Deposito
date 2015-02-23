# -*- coding: utf-8 -*-
import json

from pagador.reloaded import entidades
from pagador_deposito.reloaded import cadastro


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'email_comprovante', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total', 'json']
    _codigo_gateway = 7

    def __init__(self, loja_id, codigo_pagamento=None):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id, codigo_pagamento)
        self.preencher_do_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioDeposito()
        if not self.json:
            self.json = []
            for banco in entidades.Banco().listar_todos():
                banco_deposito = cadastro.BANCO_BASE.copy()
                banco_deposito['nome'] = banco.nome
                banco_deposito['codigo'] = banco.codigo
                banco_deposito['imagem'] = banco.imagem
                self.json.append(banco_deposito)

    @property
    def configurado(self):
        for banco in self.json:
            if self._banco_esta_configurado(banco):
                return True
        return False

    def _banco_esta_configurado(self, banco):
        configurado = (
            banco['ativo'] and
            banco['agencia'] is not None and
            banco['numero_conta'] is not None and
            banco['cpf_cnpj'] is not None and
            banco['favorecido'] is not None
        )
        if banco['codigo'] == '104':
            configurado = configurado and banco['operacao'] is not None
        return configurado