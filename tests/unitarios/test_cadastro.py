# -*- coding: utf-8 -*-
import unittest
from pagador_deposito.reloaded import cadastro


class FormularioDeposito(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FormularioDeposito, self).__init__(*args, **kwargs)
        self.formulario = cadastro.FormularioDeposito()

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

    def test_deve_ter_desconto_valor(self):
        self.formulario.desconto_valor.nome.should.be.equal('desconto_valor')
        self.formulario.desconto_valor.ordem.should.be.equal(3)
        self.formulario.desconto_valor.label.should.be.equal(u'Desconto aplicado')
        self.formulario.desconto_valor.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.decimal)

    def test_deve_ter_informacao_complementar(self):
        self.formulario.informacao_complementar.nome.should.be.equal('informacao_complementar')
        self.formulario.informacao_complementar.ordem.should.be.equal(4)
        self.formulario.informacao_complementar.label.should.be.equal(u'Informação complementar')
        self.formulario.informacao_complementar.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.area)

    def test_deve_ter_aplicar_no_total(self):
        self.formulario.aplicar_no_total.nome.should.be.equal('aplicar_no_total')
        self.formulario.aplicar_no_total.ordem.should.be.equal(5)
        self.formulario.aplicar_no_total.label.should.be.equal(u'Aplicar no total?')
        self.formulario.aplicar_no_total.tipo.should.be.equal(cadastro.cadastro.TipoDeCampo.boleano)
