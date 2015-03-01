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

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_preencher_do_gateway_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        preencher_mock.assert_called_with(configuracao, self.codigo_gateway, self.campos)

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_definir_formulario_na_inicializacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.formulario.should.be.a('pagador_deposito.reloaded.cadastro.FormularioDeposito')

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco', mock.MagicMock())
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_nao_ser_aplicacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.eh_aplicacao.should.be.falsy

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_ter_json_padrao_se_nao_tiver_ainda(self, preencher_mock, banco_mock):
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
            {'id': 1, 'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_1', 'ativo': False},
            {'id': 2, 'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
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

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_obter_banco_ativo(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': 'codigo_1', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.obter_banco_ativo('1').should.be.equal(configuracao.json[0])

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_obter_banco_ativo_retorna_erro_se_nao_for_ativo(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': 'codigo_1', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.obter_banco_ativo.when.called_with('3').should.throw(
            entidades.ConfiguracaoBancoNaoEncontrada,
            u'Não foi encontrado um banco ativo com id 3 nas configuracoes da loja 234'
        )

    @mock.patch('pagador_deposito.reloaded.entidades.entidades.Banco')
    @mock.patch('pagador_deposito.reloaded.entidades.ConfiguracaoMeioPagamento.preencher_do_gateway', autospec=True)
    def test_deve_obter_banco_ativo_retorna_erro_se_nao_achar(self, preencher_mock, banco_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.json = [
            {'id': 1, 'numero_conta': '4444', 'favorecido': 'ZES', 'imagem': 'imagem_13', 'nome': 'banco_3', 'operacao': None, 'poupanca': False, 'agencia': '555', 'cpf_cnpj': '1234568897', 'codigo': '303', 'ativo': True},
            {'id': 2, 'numero_conta': '12322', 'favorecido': 'ZAS', 'imagem': 'imagem_1', 'nome': 'banco_1', 'operacao': None, 'poupanca': False, 'agencia': '1554', 'cpf_cnpj': '1234568', 'codigo': 'codigo_1', 'ativo': True},
            {'id': 3, 'numero_conta': None, 'favorecido': None, 'imagem': 'imagem_2', 'nome': 'banco_2', 'operacao': None, 'poupanca': False, 'agencia': None, 'cpf_cnpj': None, 'codigo': 'codigo_2', 'ativo': False}
        ]
        configuracao.obter_banco_ativo.when.called_with('4').should.throw(
            entidades.ConfiguracaoBancoNaoEncontrada,
            u'Não foi encontrado um banco ativo com id 4 nas configuracoes da loja 234'
        )


class DepositoMontandoMalote(unittest.TestCase):
    def setUp(self):
        self.dados_json = [{
            'id': str(i),
            'ativo': i % 2 == 0,
            'nome': 'Banco {}'.format(i),
            'codigo': '{}{}{}'.format(i, i, i),
            'imagem': 'imagem-{}.png'.format(i),
            'agencia': '3645',
            'numero_conta': '12345',
            'poupanca': False,
            'favorecido': 'Favorecido Nome {}'.format(i),
            'operacao': None,
            'cpf_cnpj': '12345678901',
        } for i in range(1, 4)]
        self.loja_id = 23
        self.malote = entidades.Malote(mock.MagicMock(loja_id=self.loja_id, json=self.dados_json, email_comprovante='email@comprovante.com', informacao_complementar='informacao_complementar'))
        self.pedido = mock.MagicMock()
        self.pedido.numero = 1234
        self.pedido.email_contato_da_loja = 'email@contato.com'

    def test_deve_ter_propriedades(self):
        entidades.Malote('configuracao').to_dict().should.be.equal(
            {
                'banco_agencia': None, 'banco_codigo': None, 'banco_imagem': None, 'banco_nome': None,
                'numero_conta': None, 'operacao': None, 'eh_poupanca': False, 'cpf_cnpj': None,
                'favorecido': None, 'informacao_complementar': None, 'email_comprovante': None
            }
        )

    def test_deve_montar_conteudo(self):
        dados = {'banco_id': '1'}
        self.malote.configuracao.obter_banco_ativo.return_value = self.dados_json[0]
        self.malote.monta_conteudo(self.pedido, parametros_contrato=None, dados=dados)
        self.malote.to_dict().should.be.equal(
            {
                'banco_agencia': '3645', 'banco_codigo': '111', 'banco_imagem': 'imagem-1.png', 'banco_nome': 'Banco 1',
                'numero_conta': '12345', 'operacao': None, 'eh_poupanca': False, 'cpf_cnpj': '123.456.789-01',
                'favorecido': 'Favorecido Nome 1', 'informacao_complementar': 'informacao_complementar', 'email_comprovante': 'email@comprovante.com'
            }
        )

    def test_obter_email_da_conta(self):
        dados = {'banco_id': '1'}
        self.malote.configuracao.obter_banco_ativo.return_value = self.dados_json[0]
        self.malote.configuracao.email_comprovante = None
        self.malote.monta_conteudo(self.pedido, parametros_contrato=None, dados=dados)
        self.malote.to_dict().should.be.equal(
            {
                'banco_agencia': '3645', 'banco_codigo': '111', 'banco_imagem': 'imagem-1.png', 'banco_nome': 'Banco 1',
                'numero_conta': '12345', 'operacao': None, 'eh_poupanca': False, 'cpf_cnpj': '123.456.789-01',
                'favorecido': 'Favorecido Nome 1', 'informacao_complementar': 'informacao_complementar', 'email_comprovante': 'email@contato.com'
            }
        )

    def test_da_erro_se_nao_passar_banco_id(self):
        dados = {}
        self.malote.monta_conteudo.when.called_with(self.pedido, parametros_contrato=None, dados=dados).should.throw(entidades.DepositoInvalido, u'Não foi informado o banco para o depósito do pedido {} no dados.'.format(self.pedido.numero))

    def test_da_erro_se_nao_achar_banco(self):
        dados = {'banco_id': '10'}
        self.malote.configuracao.obter_banco_ativo.side_effect = entidades.ConfiguracaoBancoNaoEncontrada()
        self.malote.monta_conteudo.when.called_with(self.pedido, parametros_contrato=None, dados=dados).should.throw(
            entidades.DepositoInvalido,
            u'O banco id {} para o depósito do pedido {} não está ativo na loja {}.'.format(10, self.pedido.numero, self.loja_id)
        )
