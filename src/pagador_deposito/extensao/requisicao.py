# -*- coding: utf-8 -*-

import urllib

from pagador import settings
from pagador.envio.requisicao import Enviar
from pagador_paypal.extensao.envio import RequestNVP
from pagador_paypal.extensao.seguranca import ParametrosPayPal


class TipoAck(object):
    Sucesso = "Success"
    Falha = "Failure"


class EnviarPedido(Enviar):
    def __init__(self, pedido, dados):
        self.pedido = pedido
        RequestNVP.cria_payment_request()
        for item in range(0, len(self.pedido.itens.all())):
            RequestNVP.cria_item_payment_request(item)
        self.dados = self.gerar_dados_de_envio(dados)
        self.exige_autenticacao = True
        self.processa_resposta = True
        self.url = "https://api-3t.{}paypal.com/nvp".format("sandbox." if settings.DEBUG else "")
        self.grava_identificador = False
        self.headers = {}
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        self.envio_por_querystring = True

    def gerar_dados_de_envio(self, dados):
        notification_url = settings.PAYPAL_NOTIFICATION_URL.format(self.pedido.conta.id)
        parametros = ParametrosPayPal("paypal", id=self.pedido.conta.id)
        request_nvp = RequestNVP(
            user=parametros.username,
            pwd=parametros.password,
            signature=parametros.signature,
            buttonsource=parametros.button_source,
            email=self.pedido.cliente.email,
            returnurl="{}/success?next_url={}".format(notification_url, dados["next_url"]),
            cancelurl="{}/failure?next_url={}".format(notification_url, dados["next_url"]),
            version=settings.PAYPAL_VERSION,
            method='SetExpressCheckout',
            localecode='pt_BR',

            paymentrequest_0_paymentaction='SALE',
            paymentrequest_0_notifyurl=notification_url,
            paymentrequest_0_amt=self.utils.formata_decimal(self.pedido.valor_total),
            paymentrequest_0_shippingamt=self.utils.formata_decimal(self.pedido.valor_envio),
            paymentrequest_0_currencycode="BRL",
            paymentrequest_0_itemamt=self.utils.formata_decimal(self.pedido.valor_subtotal),
            paymentrequest_0_invnum=self.pedido.numero
        )
        for indice, item in enumerate(self.pedido.itens.all()):
            self.define_valor_de_atributo_de_item(request_nvp, "NAME", indice, item.nome[:127])
            self.define_valor_de_atributo_de_item(request_nvp, "DESC", indice, item.produto.descricao_completa[:127])
            self.define_valor_de_atributo_de_item(request_nvp, "AMT", indice, self.utils.formata_decimal(item.preco_venda))
            self.define_valor_de_atributo_de_item(request_nvp, "QTY", indice, self.utils.formata_decimal(item.quantidade))
            self.define_valor_de_atributo_de_item(request_nvp, "NUMBER", indice, item.sku[:127])
            self.define_valor_de_atributo_de_item(request_nvp, "ITEMURL", indice, item.produto.get_absolute_url())
        return request_nvp.to_dict()

    def define_valor_de_atributo_de_item(self, request_nvp, atributo, indice, valor):
        nome = "L_PAYMENTREQUEST_0_{}{}".format(atributo, indice)
        request_nvp.define_valor_de_atributo(nome, {nome.lower(): valor})

    @property
    def items(self):
        return []

    def obter_situacao_do_pedido(self, status_requisicao):
        return None

    def processar_resposta(self, resposta):
        content = resposta.content
        retorno = {}
        if content:
            content = urllib.unquote(content).decode('utf8')
            retorno = {par.split("=")[0]: par.split("=")[1] for par in content.split("&")}
        if "ACK" in retorno and retorno["ACK"] == TipoAck.Sucesso:
            url = "https://www.{}paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={}".format(("sandbox." if settings.DEBUG else ""), retorno["TOKEN"])
            return {"content": {"url": url}, "status": 200, "reenviar": False, "identificador": retorno["TOKEN"]}
        return {"content": retorno, "status": 500, "reenviar": False}
