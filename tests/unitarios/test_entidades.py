# -*- coding: utf-8 -*-
import unittest
import mock

from pagador_deposito.reloaded import entidades


class DepositoConfiguracaoMeioPagamento(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DepositoConfiguracaoMeioPagamento, self).__init__(*args, **kwargs)
        self.campos = ['ativo', 'email_comprovante', 'desconto_valor', 'informacao_complementar', 'aplicar_no_total']
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
    def test_deve_ser_aplicacao(self, preencher_mock):
        configuracao = entidades.ConfiguracaoMeioPagamento(234)
        configuracao.eh_aplicacao.should.be.falsy
