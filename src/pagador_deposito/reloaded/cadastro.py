# -*- coding: utf-8 -*-

from li_common.padroes import cadastro


class FormularioDeposito(cadastro.Formulario):
    ativo = cadastro.CampoFormulario('ativo', 'Pagamento ativo?', requerido=True, tipo=cadastro.TipoDeCampo.boleano, ordem=1)
    email_comprovante = cadastro.CampoFormulario('email_comprovante', u'E-mail para comprovante', requerido=False, tamanho_max=128, ordem=2)
    desconto_valor = cadastro.CampoFormulario('desconto_valor', u'Desconto aplicado', requerido=False, ordem=3, tipo=cadastro.TipoDeCampo.decimal)
    informacao_complementar = cadastro.CampoFormulario('informacao_complementar', u'Informação complementar', requerido=False, ordem=4, tipo=cadastro.TipoDeCampo.area, texto_ajuda=u'Esta informação será apresentada junto dos dados bancários para o cliente.')
    aplicar_no_total = cadastro.CampoFormulario('aplicar_no_total', u'Aplicar no total?', requerido=False, ordem=5, tipo=cadastro.TipoDeCampo.boleano, texto_ajuda=u'Aplicar desconto no total da compra (incluir por exemplo o frete).')
