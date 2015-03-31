# -*- coding: utf-8 -*-
import unittest

import mock

from pagador_deposito import entidades


class DepositoConfiguracaoMeioPagamento(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DepositoConfiguracaoMeioPagamento, self).__init__(*args, **kwargs)
        self.campos = ['ativo', 'email_comprovante', 'desconto', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total', 'json']
        self.codigo_gateway = 7

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_ter_os_campos_especificos_na_classe(self):
        entidades.ConfiguracaoMeioPagamento(234).campos.should.be.equal(self.campos)

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_ter_codigo_gateway(self):
        entidades.ConfiguracaoMeioPagamento(234).codigo_gateway.should.be.equal(self.codigo_gateway)

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', autospec=True)
    def test_deve_preencher_gateway_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        preencher_mock.assert_called_with(configuracao, self.codigo_gateway, self.campos)

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_definir_formulario_na_inicializacao(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.formulario.should.be.a('pagador_deposito.cadastro.FormularioDeposito')

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_nao_ser_aplicacao(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.eh_aplicacao.should.be.falsy

    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.entidades.Banco')
    def test_deve_ter_json_padrao_se_nao_tiver_ainda(self, banco_mock):
        banco_listar = mock.MagicMock()
        banco_1 = mock.MagicMock()
        banco_1.id = 1
        banco_1.nome = 'banco_1'
        banco_1.codigo = 'codigo_1'
        banco_1.imagem = 'imagem_1'
        banco_2 = mock.MagicMock()
        banco_2.id = 2
        banco_2.nome = 'banco_2'
        banco_2.codigo = 'codigo_2'
        banco_2.imagem = 'imagem_2'
        banco_mock.return_value = banco_listar
        banco_listar.listar_todos.return_value = [banco_1, banco_2]
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json.should.be.equal([
            {'id': 1, 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False},
            {'id': 2, 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ])

    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.entidades.Banco')
    def test_deve_montar_lista_de_bancos_mesclando_com_json_vazio(self, banco_mock):
        banco_mock.return_value.listar_todos.return_value = [
            mock.MagicMock(id=1, nome='Banco 1', codigo='101', imagem='imagem01.png'),
            mock.MagicMock(id=2, nome='Banco 2', codigo='102', imagem='imagem02.png'),
        ]
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.bancos.should.be.equal([
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem01.png', 'nome': 'Banco 1', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': '101', 'ativo': False, 'id': 1},
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem02.png', 'nome': 'Banco 2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': '102', 'ativo': False, 'id': 2}
        ])

    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.entidades.Banco')
    def test_deve_dizer_que_nao_esta_configurado(self, banco_mock):
        banco_mock.return_value.listar_todos.return_value = [
            mock.MagicMock(id=1, nome='Banco 1', codigo='101', imagem='imagem01.png'),
            mock.MagicMock(id=2, nome='Banco 2', codigo='102', imagem='imagem02.png'),
        ]
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.configurado.should.be.falsy

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_dizer_que_nao_estah_configurado_se_json_for_none(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = None
        configuracao.configurado.should.be.falsy

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_dizer_que_estah_configurado(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': '1', 'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True},
            {'id': '2', 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ]
        configuracao.configurado.should.be.truthy

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_operacao_nao_pode_none_se_banco_for_104(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': '6', 'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True},
            {'id': '1', 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ]
        configuracao.configurado.should.be.falsy

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_banco_104_validar_operacao(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': '001', 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True, 'id': 6},
            {'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False, 'id': 3}
        ]
        configuracao.configurado.should.be.truthy

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_obter_dados_deposito_ativo(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ]
        configuracao.obter_dados_deposito_ativo('1').should.be.equal(configuracao.json[0])

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_obter_dados_deposito_ativo_retorna_erro_se_nao_for_ativo(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ]
        configuracao.obter_dados_deposito_ativo.when.called_with('3').should.throw(
            entidades.ConfiguracaoBancoNaoEncontrada,
            u'Não foi encontrado um banco ativo com id 3 nas configuracoes da loja 234'
        )

    @mock.patch('pagador_deposito.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.entidades.ConfiguracaoMeioPagamento.preencher_gateway', mock.MagicMock())
    def test_deve_obter_dados_deposito_ativo_retorna_erro_se_nao_achar(self):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'ativo': False}
        ]
        configuracao.obter_dados_deposito_ativo.when.called_with('4').should.throw(
            entidades.ConfiguracaoBancoNaoEncontrada,
            u'Não foi encontrado um banco ativo com id 4 nas configuracoes da loja 234'
        )


class DepositoMontandoMalote(unittest.TestCase):
    def setUp(self):
        self.dados_json = [{
            'id': str(i),
            'ativo': i % 2 == 0,
            'agencia': '3645',
            'numero_conta': '12345',
            'poupanca': False,
            'favorecido': 'Favorecido Nome {}'.format(i),
            'operacao': None,
            'cpf_cnpj': '12345678901',
        } for i in range(1, 4)]
        self.banco = mock.MagicMock(
            nome='Banco Zas',
            codigo='100',
            imagem='imagem-zas.png'
        )
        self.loja_id = 23
        self.malote = entidades.Malote(mock.MagicMock(loja_id=self.loja_id, json=self.dados_json, email_comprovante='email@comprovante.com', informacao_complementar='informacao_complementar'))
        self.pedido = mock.MagicMock()
        self.pedido.numero = 1234
        self.pedido.email_contato_loja = 'email@contato.com'

    @mock.patch('pagador.entidades.Banco', mock.MagicMock())
    def test_deve_ter_propriedades(self):
        entidades.Malote('configuracao').to_dict().should.be.equal(
            {
                'banco_agencia': None, 'banco_codigo': None, 'banco_imagem': None, 'banco_nome': None,
                'numero_conta': None, 'operacao': None, 'eh_poupanca': False, 'cpf_cnpj': None,
                'favorecido': None, 'informacao_complementar': None, 'email_comprovante': None
            }
        )

    @mock.patch('pagador.entidades.Banco')
    def test_deve_montar_conteudo(self, banco_mock):
        banco_mock.return_value = self.banco
        dados = {'banco_id': '1'}
        self.malote.configuracao.obter_dados_deposito_ativo.return_value = self.dados_json[0]
        self.malote.monta_conteudo(self.pedido, parametros_contrato=None, dados=dados)
        self.malote.to_dict().should.be.equal({'banco_agencia': '3645', 'banco_codigo': '100', 'banco_imagem': 'imagem-zas.png', 'banco_nome': 'Banco Zas', 'cpf_cnpj': '123.456.789-01', 'eh_poupanca': False, 'email_comprovante': 'email@comprovante.com', 'favorecido': 'Favorecido Nome 1', 'informacao_complementar': 'informacao_complementar', 'numero_conta': '12345', 'operacao': None})

    @mock.patch('pagador.entidades.Banco')
    def test_obter_email_conta(self, banco_mock):
        banco_mock.return_value = self.banco
        dados = {'banco_id': '1'}
        self.malote.configuracao.obter_dados_deposito_ativo.return_value = self.dados_json[0]
        self.malote.configuracao.email_comprovante = None
        self.malote.monta_conteudo(self.pedido, parametros_contrato=None, dados=dados)
        self.malote.to_dict().should.be.equal({'banco_agencia': '3645', 'banco_codigo': '100', 'banco_imagem': 'imagem-zas.png', 'banco_nome': 'Banco Zas', 'cpf_cnpj': '123.456.789-01', 'eh_poupanca': False, 'email_comprovante': 'email@contato.com', 'favorecido': 'Favorecido Nome 1', 'informacao_complementar': 'informacao_complementar', 'numero_conta': '12345', 'operacao': None})

    @mock.patch('pagador.entidades.Banco', mock.MagicMock())
    def test_dah_erro_se_nao_passar_banco_id(self):
        dados = {}
        self.malote.monta_conteudo.when.called_with(self.pedido, parametros_contrato=None, dados=dados).should.throw(entidades.DepositoInvalido, u'Não foi informado o banco para o depósito do pedido {} no dados.'.format(self.pedido.numero))

    @mock.patch('pagador.entidades.Banco', mock.MagicMock())
    def test_dah_erro_se_nao_achar_banco(self):
        dados = {'banco_id': '10'}
        self.malote.configuracao.obter_dados_deposito_ativo.side_effect = entidades.ConfiguracaoBancoNaoEncontrada()
        self.malote.monta_conteudo.when.called_with(self.pedido, parametros_contrato=None, dados=dados).should.throw(
            entidades.DepositoInvalido,
            u'O banco id {} para o depósito do pedido {} não está ativo na loja {}.'.format(10, self.pedido.numero, self.loja_id)
        )
