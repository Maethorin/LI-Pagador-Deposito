# -*- coding: utf-8 -*-
import os
from django.db import IntegrityError

from pagador.configuracao.cadastro import CampoFormulario, FormularioBase, TipoDeCampo, CadastroBase, SelecaoBase
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

    def complemento(self, dados):
        if not 'banco_id' in dados:
            return None
        if not 'metodo' in dados:
            return None
        banco_pagamento, criado = self.configuracao.bancos_configurados_na_conta(int(dados['banco_id']))
        if dados["metodo"].lower() == 'delete':
            banco_pagamento.delete()
            return {"status": 200, "content": "Banco removido com sucesso."}
        cpf, cnpj = self.trata_cpf_cnpj(dados["cpf_cnpj"])
        erro = None
        if dados["cpf_cnpj"] and not cpf and not cnpj:
            erro = {"status": 400, "content": u"CPF ou CNPJ inválido"}
        if erro:
            if criado:
                banco_pagamento.delete()
            return erro
        banco_pagamento.ativo = (dados["ativo"] == 'true')
        banco_pagamento.agencia = dados["agencia"]
        banco_pagamento.numero_conta = dados["numero_conta"]
        banco_pagamento.poupanca = dados["poupanca"]
        banco_pagamento.cpf = cpf
        banco_pagamento.cnpj = cnpj
        banco_pagamento.favorecido = dados["favorecido"]
        banco_pagamento.save()
        return {"status": 200, "content": "Banco salvo com sucesso."}

    def to_dict(self):
        return {
            "contexto": self.contexto,
            "html": [
                self.descricao_para_lojista.to_dict(),
                self.lista_bancos.to_dict()
            ]
        }

    def trata_cpf_cnpj(self, cpf_cnpj):
        if not cpf_cnpj:
            return None, None
        cpf_cnpj = ''.join([x for x in cpf_cnpj if x.isdigit()])
        cpf = None
        cnpj = None
        if len(cpf_cnpj) == 11:
            cpf = cpf_cnpj
        elif len(cpf_cnpj) == 14:
            cnpj = cpf_cnpj
        return cpf, cnpj


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
        return Script(tipo=TipoScript.html, caminho_arquivo=caminho_do_arquivo_de_template("mensagens.html"), eh_template=True)

    def to_dict(self):
        return [
            self.css.to_dict(),
            self.function_enviar.to_dict(),
            self.mensagens.to_dict()
        ]


class MeioPagamentoSelecao(SelecaoBase):
    selecao = Script(tipo=TipoScript.html, nome="selecao", caminho_arquivo=caminho_do_arquivo_de_template("selecao.html"), eh_template=True)

    def to_dict(self):
        return [
            self.selecao.to_dict()
        ]
