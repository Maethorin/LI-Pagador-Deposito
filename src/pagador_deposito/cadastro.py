# -*- coding: utf-8 -*-

from li_common.padroes import cadastro


BANCO_BASE = {
    'id': None,
    'ativo': False,
    'agencia': None,
    'numero_conta': None,
    'poupanca': False,
    'cpf_cnpj': None,
    'favorecido': None,
    'operacao': None,
}


class BancosValidador(cadastro.ValidadorBase):
    @property
    def eh_valido(self):
        valido = True
        if type(self.valor) is not list:
            valido = False
            self.erros['lista'] = 'Os bancos devem ser uma lista.'
        for banco in self.valor:
            erros = []
            for chave in BANCO_BASE:
                if chave not in banco:
                    valido = False
                    erros.append(u'Não foi enviado o atributo {} do banco {}'.format(chave, banco))
            if erros:
                self.erros['atributos'] = erros
        return valido


class DescontoValidador(cadastro.ValidadorBase):
    @property
    def eh_valido(self):
        try:
            valor = float(self.valor)
            if valor > 100.0 or valor < 0.0:
                self.erros = u'Porcentagem inválida. Insira um valor entre 0% e 100%.'
        except (TypeError, ValueError):
            self.erros = u'Porcentagem inválida. Insira um valor entre 0% e 100%.'
        return not self.erros


class FormularioDeposito(cadastro.Formulario):
    bancos = cadastro.CampoFormulario('json', ordem=0, tipo=cadastro.TipoDeCampo.oculto, formato=cadastro.FormatoDeCampo.json, validador=BancosValidador)

    ativo = cadastro.CampoFormulario('ativo', 'Pagamento ativo?', tipo=cadastro.TipoDeCampo.boleano, ordem=1)
    email_comprovante = cadastro.CampoFormulario('email_comprovante', u'E-mail para comprovante', requerido=False, tamanho_max=128, ordem=2)
    tem_desconto = cadastro.CampoFormulario('desconto', u'Usar desconto?', requerido=False, ordem=3, tipo=cadastro.TipoDeCampo.boleano, texto_ajuda=u'Define se o depósito usará desconto.')
    desconto_valor = cadastro.CampoFormulario('desconto_valor', u'Desconto aplicado', requerido=False, ordem=4, tipo=cadastro.TipoDeCampo.decimal, validador=DescontoValidador)
    informacao_complementar = cadastro.CampoFormulario('informacao_complementar', u'Informação complementar', requerido=False, ordem=5, tipo=cadastro.TipoDeCampo.area, texto_ajuda=u'Esta informação será apresentada junto dos dados bancários para o cliente.')
    aplicar_no_total = cadastro.CampoFormulario('aplicar_no_total', u'Aplicar no total?', requerido=False, ordem=6, tipo=cadastro.TipoDeCampo.boleano, texto_ajuda=u'Aplicar desconto no total da compra (incluir por exemplo o frete).')


