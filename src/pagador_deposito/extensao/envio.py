# -*- coding: utf-8 -*-
from pagador.envio.serializacao import EntidadeSerializavel, Atributo


class RequestNVP(EntidadeSerializavel):
    atributos = [
        Atributo("USER"), Atributo("PWD"), Atributo("SIGNATURE"), Atributo("VERSION"), Atributo("SUBJECT"), Atributo("METHOD"),
        Atributo("RETURNURL"), Atributo("CANCELURL"), Atributo("BUTTONSOURCE"), Atributo("LOCALECODE"), Atributo("HDRIMG"), Atributo("EMAIL")
    ]

    @classmethod
    def cria_payment_request(cls, indice=0):
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_PAYMENTACTION".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_AMT".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPPINGAMT".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_CURRENCYCODE".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_ITEMAMT".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_INVNUM".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_NOTIFYURL".format(indice)))

    @classmethod
    def cria_shipto(cls, indice=0):
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTONAME".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOSTREET".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOSTREET2".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOCITY".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOSTATE".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOZIP".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOCOUNTRYCODE".format(indice)))
        cls.atributos.append(Atributo("PAYMENTREQUEST_{}_SHIPTOPHONENUM".format(indice)))

    @classmethod
    def cria_item_payment_request(cls, item, indice=0):
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_NAME{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_DESC{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_AMT{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_QTY{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_NUMBER{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMURL{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMWEIGHTVALUE{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMWEIGHTUNIT{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMLENGTHVALUE{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMLENGTHUNIT{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMWIDTHVALUE{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMWIDTHUNIT{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMHEIGHTVALUE{}".format(indice, item)))
        cls.atributos.append(Atributo("L_PAYMENTREQUEST_{}_ITEMHEIGHTUNIT{}".format(indice, item)))
