# -*- coding: utf-8 -*-

from li_common.padroes import cadastro


BANCO_BASE = {
    'id': None,
    'nome': None,
    'imagem': None,
    'codigo': None,
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


class FormularioDeposito(cadastro.Formulario):
    bancos = cadastro.CampoFormulario('json', ordem=0, tipo=cadastro.TipoDeCampo.oculto, formato=cadastro.FormatoDeCampo.json, validador=BancosValidador)

    ativo = cadastro.CampoFormulario('ativo', 'Pagamento ativo?', requerido=True, tipo=cadastro.TipoDeCampo.boleano, ordem=1)
    email_comprovante = cadastro.CampoFormulario('email_comprovante', u'E-mail para comprovante', requerido=False, tamanho_max=128, ordem=2)
    desconto_valor = cadastro.CampoFormulario('desconto_valor', u'Desconto aplicado', requerido=False, ordem=3, tipo=cadastro.TipoDeCampo.decimal)
    informacao_complementar = cadastro.CampoFormulario('informacao_complementar', u'Informação complementar', requerido=False, ordem=4, tipo=cadastro.TipoDeCampo.area, texto_ajuda=u'Esta informação será apresentada junto dos dados bancários para o cliente.')
    aplicar_no_total = cadastro.CampoFormulario('aplicar_no_total', u'Aplicar no total?', requerido=False, ordem=5, tipo=cadastro.TipoDeCampo.boleano, texto_ajuda=u'Aplicar desconto no total da compra (incluir por exemplo o frete).')
