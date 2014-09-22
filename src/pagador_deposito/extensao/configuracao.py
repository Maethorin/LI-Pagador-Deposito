# -*- coding: utf-8 -*-
import os

from pagador.configuracao.cadastro import CampoFormulario, FormularioBase, TipoDeCampo, CadastroBase
from pagador.configuracao.cliente import Script, TipoScript


def caminho_do_arquivo_de_template(arquivo):
    diretorio = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(diretorio, "templates", arquivo)


class MeioPagamentoCadastro(CadastroBase):
    lista_bancos = Script(tipo=TipoScript.html, eh_template=True, nome="complemento", caminho_arquivo=caminho_do_arquivo_de_template("lista_bancos.html"))

    @property
    def descricao_para_lojista(self):
        script = Script(tipo=TipoScript.html, nome="descricao")
        script.adiciona_linha('<p>Ative um ou mais bancos abaixo para que a forma de pagamento por Depósito seja habilitada na sua loja</p>')
        return script

    @property
    def contexto(self):
        bancos = []
        for banco in self.configuracao.bancos:
            banco_dict = {'id': banco.id, 'nome': banco.nome, 'imagem': banco.imagem, 'codigo': banco.codigo}
            if hasattr(banco, 'pagamento_banco'):
                banco_dict['pagamento_banco'] = {
                    'ativo': banco.pagamento_banco.ativo,
                    'agencia': banco.pagamento_banco.agencia,
                    'numero_conta': banco.pagamento_banco.numero_conta,
                    'poupanca': banco.pagamento_banco.poupanca,
                    'cpf_cnpj': banco.pagamento_banco.cpf_cnpj,
                    'favorecido': banco.pagamento_banco.favorecido,
                }
            bancos.append(banco_dict)
        return {'bancos': bancos}

    def to_dict(self):
        return {
            "contexto": self.contexto,
            "html": [
                self.descricao_para_lojista.to_dict(),
                self.lista_bancos.to_dict()
            ]
        }


class Formulario(FormularioBase):
    email_comprovante = CampoFormulario("usuario", u"E-mail para comprovante", requerido=False, tamanho_max=128, ordem=1)
    desconto_valor = CampoFormulario("desconto_valor", u"Desconto aplicado", requerido=False, ordem=2, tipo=TipoDeCampo.decimal)
    informacao_complementar = CampoFormulario("informacao_complementar", u"Informação complementar", requerido=False, ordem=3, tipo=TipoDeCampo.area, texto_ajuda=u"Esta informação será apresentada junto dos dados bancários para o cliente.")
    aplicar_no_total = CampoFormulario("aplicar_no_total", u"Aplicar no total?", requerido=False, ordem=4, tipo=TipoDeCampo.boleano, texto_ajuda=u"Aplicar desconto no total da compra (incluir por exemplo o frete).")


class MeioPagamentoEnvio(object):
    @property
    def css(self):
        return Script(tipo=TipoScript.css, caminho_arquivo=caminho_do_arquivo_de_template("style.css"))

    @property
    def function_enviar(self):
        return Script(tipo=TipoScript.javascript, eh_template=True, caminho_arquivo=caminho_do_arquivo_de_template("javascript.js"))

    @property
    def mensagens(self):
        return Script(tipo=TipoScript.html, caminho_arquivo=caminho_do_arquivo_de_template("mensagens.html"))

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]


class MeioPagamentoSelecao(object):
    logo = Script(tipo=TipoScript.html, nome="logo", conteudo=u'<img src="{{ STATIC_URL }}novo-template/img/bandeiras/paypal.png" alt="Pague com PayPal" title="Pague com PayPal" />', eh_template=True)

    @property
    def bandeiras(self):
        bandeiras = Script(tipo=TipoScript.html, nome="explicativo")
        bandeiras.adiciona_linha('<ul class="bandeiras-pagamento">')
        bandeiras.adiciona_linha('    <li><i class="icone-pagamento visa" title="Visa"></i></li>')
        bandeiras.adiciona_linha('    <li><i class="icone-pagamento mastercard" title="Mastercard"></i></li>')
        bandeiras.adiciona_linha('</ul>')
        return bandeiras

    def to_dict(self):
        return [
            self.logo.to_dict(),
            self.bandeiras.to_dict()
        ]
