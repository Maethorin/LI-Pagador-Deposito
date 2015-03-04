# -*- coding: utf-8 -*-
import json

from pagador.reloaded import entidades
from pagador_deposito.reloaded import cadastro

CODIGO_GATEWAY = 7

class DepositoInvalido(Exception):
    pass


class Malote(entidades.Malote):
    def __init__(self, configuracao):
        super(Malote, self).__init__(configuracao)
        self.email_comprovante = None
        self.banco_nome = None
        self.banco_codigo = None
        self.banco_imagem = None
        self.banco_agencia = None
        self.numero_conta = None
        self.eh_poupanca = False
        self.favorecido = None
        self.operacao = None
        self.cpf_cnpj = None
        self.informacao_complementar = None

    def monta_conteudo(self, pedido, parametros_contrato=None, dados=None):
        try:
            banco_id = dados['banco_id']
        except KeyError:
            raise DepositoInvalido(u'Não foi informado o banco para o depósito do pedido {} no dados.'.format(pedido.numero))
        try:
            banco = self.configuracao.obter_banco_ativo(banco_id)
        except ConfiguracaoBancoNaoEncontrada:
            raise DepositoInvalido(u'O banco id {} para o depósito do pedido {} não está ativo na loja {}.'.format(banco_id, pedido.numero, self.configuracao.loja_id))

        self.email_comprovante = self.configuracao.email_comprovante
        if not self.email_comprovante:
            self.email_comprovante = pedido.email_contato_loja
        self.banco_nome = self.formatador.trata_unicode_com_limite(banco['nome'])
        self.banco_codigo = banco['codigo']
        self.banco_imagem = banco['imagem']
        self.banco_agencia = banco['agencia']
        self.numero_conta = banco['numero_conta']
        self.eh_poupanca = banco['poupanca']
        self.favorecido = self.formatador.trata_unicode_com_limite(banco['favorecido'])
        self.operacao = banco['operacao']
        self.cpf_cnpj = self.formatador.formata_cpf_cnpj(banco['cpf_cnpj'])
        self.informacao_complementar = self.formatador.trata_unicode_com_limite(self.configuracao.informacao_complementar)


class ConfiguracaoBancoNaoEncontrada(Exception):
    pass


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    _campos = ['ativo', 'email_comprovante', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total', 'json']
    _codigo_gateway = CODIGO_GATEWAY

    def __init__(self, loja_id, codigo_pagamento=None):
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id, codigo_pagamento)
        self.preencher_gateway(self._codigo_gateway, self._campos)
        self.formulario = cadastro.FormularioDeposito()
        if not self.json:
            self.json = []
            for banco in entidades.Banco().listar_todos():
                banco_deposito = cadastro.BANCO_BASE.copy()
                banco_deposito['id'] = banco.id
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

    def obter_banco_ativo(self, banco_id):
        for banco in self.json:
            if int(banco_id) == int(banco['id']) and banco['ativo']:
                return banco
        raise ConfiguracaoBancoNaoEncontrada(u'Não foi encontrado um banco ativo com id {} nas configuracoes da loja {}'.format(banco_id, self.loja_id))

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