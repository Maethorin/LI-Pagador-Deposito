# -*- coding: utf-8 -*-
import unittest

from pagador_deposito import cadastro


class FormularioDeposito(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FormularioDeposito, self).__init__(*args, **kwargs)
        self.formulario = cadastro.FormularioDeposito()

    def test_deve_ter_bancos(self):
        self.formulario.bancos.nome.should.be.equal('json')
        self.formulario.bancos.ordem.should.be.equal(0)
        self.formulario.bancos.formato.should.be.equal(cadastro.cadastro.FormatoDeCampo.json)
        self.formulario.bancos.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.oculto)
        self.formulario.bancos.validador.should.be.equal(cadastro.BancosValidador)

    def test_deve_ter_ativo(self):
        self.formulario.ativo.nome.should.be.equal('ativo')
        self.formulario.ativo.ordem.should.be.equal(1)
        self.formulario.ativo.label.should.be.equal('Pagamento ativo?')
        self.formulario.ativo.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)

    def test_deve_ter_email_comprovante(self):
        self.formulario.email_comprovante.nome.should.be.equal('email_comprovante')
        self.formulario.email_comprovante.ordem.should.be.equal(2)
        self.formulario.email_comprovante.label.should.be.equal(u'E-mail para comprovante')
        self.formulario.email_comprovante.tamanho_max.should.be.equal(128)

    def test_deve_ter_desconto(self):
        self.formulario.tem_desconto.nome.should.be.equal('desconto')
        self.formulario.tem_desconto.ordem.should.be.equal(3)
        self.formulario.tem_desconto.label.should.be.equal(u'Usar desconto?')
        self.formulario.tem_desconto.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)

    def test_deve_ter_desconto_valor(self):
        self.formulario.desconto_valor.nome.should.be.equal('desconto_valor')
        self.formulario.desconto_valor.ordem.should.be.equal(4)
        self.formulario.desconto_valor.label.should.be.equal(u'Desconto aplicado')
        self.formulario.desconto_valor.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.decimal)
        self.formulario.desconto_valor.validador.should.be.equal(cadastro.DescontoValidador)

    def test_deve_ter_informacao_complementar(self):
        self.formulario.informacao_complementar.nome.should.be.equal('informacao_complementar')
        self.formulario.informacao_complementar.ordem.should.be.equal(5)
        self.formulario.informacao_complementar.label.should.be.equal(u'Informação complementar')
        self.formulario.informacao_complementar.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.area)

    def test_deve_ter_aplicar_no_total(self):
        self.formulario.aplicar_no_total.nome.should.be.equal('aplicar_no_total')
        self.formulario.aplicar_no_total.ordem.should.be.equal(6)
        self.formulario.aplicar_no_total.label.should.be.equal(u'Aplicar no total?')
        self.formulario.aplicar_no_total.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)


class ValidadorBancos(unittest.TestCase):
    def test_deve_adicionar_erro_se_nao_for_lista(self):
        validador = cadastro.BancosValidador(valor='nao-eh-lista')
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.contain('lista')
        validador.erros['lista'].should.be.equal('Os bancos devem ser uma lista.')

    def test_deve_adicionar_erro_para_atributos_faltando(self):
        validador = cadastro.BancosValidador(valor=['faltando'])
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.be.equal({
            'atributos': [
                u'Não foi enviado o atributo numero_conta do banco faltando',
                u'Não foi enviado o atributo agencia do banco faltando',
                u'Não foi enviado o atributo favorecido do banco faltando',
                u'Não foi enviado o atributo cpf_cnpj do banco faltando',
                u'Não foi enviado o atributo operacao do banco faltando',
                u'Não foi enviado o atributo ativo do banco faltando',
                u'Não foi enviado o atributo id do banco faltando',
                u'Não foi enviado o atributo poupanca do banco faltando'
            ]
        })

    def test_deve_ser_valido_se_conter_todos_os_atributos(self):
        validador = cadastro.BancosValidador(valor=[cadastro.BANCO_BASE.copy()])
        validador.eh_valido.should.be.equal(True)
        validador.erros.should.be.empty


class ValidarDesconto(unittest.TestCase):
    def test_deve_validar_maior_que_100(self):
        validador = cadastro.DescontoValidador(valor='123.94')
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.be.equal(u'Porcentagem inválida. Insira um valor entre 0% e 100%.')

    def test_deve_validar_menor_que_0(self):
        validador = cadastro.DescontoValidador(valor='-0.5')
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.be.equal(u'Porcentagem inválida. Insira um valor entre 0% e 100%.')

    def test_deve_validar_none(self):
        validador = cadastro.DescontoValidador(valor=None)
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.be.equal(u'Porcentagem inválida. Insira um valor entre 0% e 100%.')

    def test_deve_validar_se_valor_gerar_value_error(self):
        validador = cadastro.DescontoValidador(valor='asdds')
        validador.eh_valido.should.be.equal(False)
        validador.erros.should.be.equal(u'Porcentagem inválida. Insira um valor entre 0% e 100%.')

    def test_deve_retornar_ok_se_valor_for_certo(self):
        validador = cadastro.DescontoValidador(valor='50.43444')
        validador.eh_valido.should.be.equal(True)
        validador.erros.should.be.empty