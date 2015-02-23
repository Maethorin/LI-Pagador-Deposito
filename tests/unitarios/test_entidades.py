# -*- coding: utf-8 -*-
import unittest
import mock

from pagador_deposito.reloaded import entidades


class DepositoConfiguracaoMeioPagamento(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DepositoConfiguracaoMeioPagamento, self).__init__(*args, **kwargs)
        self.campos = ['ativo', 'email_comprovante', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total', 'json']
        self.codigo_gateway = 7

    def test_deve_ter_os_campos_especificos_na_classe(self):
        entidades.ConfiguracaoMeioPagamento._campos.should.be.equal(self.campos)

    def test_deve_ter_codigo_gateway(self):
        entidades.ConfiguracaoMeioPagamento._codigo_gateway.should.be.equal(self.codigo_gateway)

    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_preencher_do_gateway_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        preencher_mock.assert_called_with(configuracao, self.codigo_gateway, self.campos)

    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_definir_formulario_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.formulario.should.be.a('pagador_deposito.reloaded.cadastro.FormularioDeposito')

    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_nao_ser_aplicacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.eh_aplicacao.should.be.falsy

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_ter_json_padrao_se_nao_tiver_ainda(self, preencher_mock, banco_mock):
        banco_listar = mock.MagicMock()
        banco_1 = mock.MagicMock()
        banco_1.nome = 'banco_1'
        banco_1.codigo = 'codigo_1'
        banco_1.imagem = 'imagem_1'
        banco_2 = mock.MagicMock()
        banco_2.nome = 'banco_2'
        banco_2.codigo = 'codigo_2'
        banco_2.imagem = 'imagem_2'
        banco_mock.return_value = banco_listar
        banco_listar.listar_todos.return_value = [banco_1, banco_2]
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json.should.be.equal([
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_1', 'ativo': False},
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ])

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_dizer_que_esta_configurado(self, preencher_mock, banco_mock):
        banco_listar = mock.MagicMock()
        banco_1 = mock.MagicMock()
        banco_1.nome = 'banco_1'
        banco_1.codigo = 'codigo_1'
        banco_1.imagem = 'imagem_1'
        banco_2 = mock.MagicMock()
        banco_2.nome = 'banco_2'
        banco_2.codigo = 'codigo_2'
        banco_2.imagem = 'imagem_2'
        banco_mock.return_value = banco_listar
        banco_listar.listar_todos.return_value = [banco_1, banco_2]
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.configurado.should.be.falsy

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_dizer_que_estah_configurado(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': 'codigo_1', 'ativo': True},
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.configurado.should.be.truthy

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_operacao_nao_pode_none_se_banco_for_104(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': '104', 'ativo': True},
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.configurado.should.be.falsy

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_banco_104_de_validar_operacao(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': '001', 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': '104', 'ativo': True},
            {'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.configurado.should.be.truthy
