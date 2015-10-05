# -*- coding: utf-8 -*-

from pagador import entidades
from pagador_deposito import cadastro

CODIGO_GATEWAY = 7


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
            raise self.DadosInvalidos(u'Não foi informado o banco para o depósito do pedido {} no dados.'.format(pedido.numero))
        try:
            dados_deposito = self.configuracao.obter_dados_deposito_ativo(banco_id)
        except ConfiguracaoBancoNaoEncontrada:
            raise self.DadosInvalidos(u'O banco escolhido para o depósito do pedido não está mais ativo na loja.'.format(pedido.numero))

        self.email_comprovante = self.configuracao.email_comprovante
        if not self.email_comprovante:
            self.email_comprovante = pedido.email_contato_loja
        banco = entidades.Banco(banco_id=dados['banco_id'])
        self.banco_nome = self.formatador.trata_unicode_com_limite(banco.nome)
        self.banco_codigo = banco.codigo
        self.banco_imagem = banco.imagem
        self.banco_agencia = dados_deposito['agencia']
        self.numero_conta = dados_deposito['numero_conta']
        self.eh_poupanca = dados_deposito['poupanca']
        self.favorecido = self.formatador.trata_unicode_com_limite(dados_deposito['favorecido'])
        self.operacao = dados_deposito['operacao']
        self.cpf_cnpj = self.formatador.formata_cpf_cnpj(dados_deposito['cpf_cnpj'])
        self.informacao_complementar = self.formatador.trata_unicode_com_limite(self.configuracao.informacao_complementar)


class ConfiguracaoBancoNaoEncontrada(Exception):
    pass


class ConfiguracaoMeioPagamento(entidades.ConfiguracaoMeioPagamento):
    modos_pagamento_aceitos = {
        'bancos': [],
    }

    def __init__(self, loja_id, codigo_pagamento=None, eh_listagem=False):
        self.campos = ['ativo', 'email_comprovante', 'desconto', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total', 'json']
        self.codigo_gateway = CODIGO_GATEWAY
        self.eh_gateway = True
        self.modos_pagamento_aceitos = {
            'bancos': [],
        }
        self._bancos = []
        self._lista_bancos = entidades.Banco().listar_todos()
        super(ConfiguracaoMeioPagamento, self).__init__(loja_id, codigo_pagamento, eh_listagem=eh_listagem)
        if not self.json:
            self.json = []
        if not self.eh_listagem:
            self.formulario = cadastro.FormularioDeposito()
            if not self.json:
                for banco in self._lista_bancos:
                    banco_deposito = cadastro.BANCO_BASE.copy()
                    banco_deposito['id'] = banco.id
                    self.json.append(banco_deposito)

    @property
    def bancos(self):
        if not self._bancos:
            for banco_deposito in self.json:
                for banco in self._lista_bancos:
                    if banco.id == int(banco_deposito['id']):
                        _banco = banco_deposito.copy()
                        _banco['codigo'] = banco.codigo
                        _banco['nome'] = banco.nome
                        _banco['imagem'] = banco.imagem
                        self._bancos.append(_banco)
        return self._bancos

    @property
    def configurado(self):
        if not self.json:
            return False
        for banco in self.json:
            if self._banco_esta_configurado(banco):
                return True
        return False

    def atualiza_meios_pagamento(self):
        if not self.json:
            return
        for banco in self.json:
            if self._banco_esta_configurado(banco):
                banco_nome = [_banco['nome'] for _banco in self.bancos if banco['id'] == _banco['id']][0]
                self.modos_pagamento_aceitos['bancos'].append(self.formatador.slugify(banco_nome))

    def obter_dados_deposito_ativo(self, banco_id):
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
        if banco['id'] == '6':
            configurado = configurado and banco['operacao'] is not None
        return configurado