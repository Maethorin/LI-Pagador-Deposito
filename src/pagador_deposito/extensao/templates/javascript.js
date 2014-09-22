//{% load filters %}
var url = '';
var $counter = null;
var segundos = 5;
$(function() {
    var $payPalMensagem = $(".paypal-mensagem");

    function iniciaContador() {
        $counter = $payPalMensagem.find(".segundos");
        setInterval('if (segundos > 0) { $counter.text(--segundos); }', 1000);
    }

    function enviaPagamento() {
        $payPalMensagem.find(".msg-danger").hide();
        $payPalMensagem.find(".msg-success").hide();
        $payPalMensagem.find(".msg-warning").show();
        $payPalMensagem.removeClass("alert-message-success");
        $payPalMensagem.removeClass("alert-message-danger");
        $payPalMensagem.addClass("alert-message-warning");
        var url_pagar = '{% url_loja "checkout_pagador" pedido.numero pagamento.id %}?next_url=' + window.location.href.split("?")[0];
        $.getJSON(url_pagar)
            .fail(function (data) {
                exibeMensagemErro(data.status, data.content);
            })
            .done(function (data) {
                console.log(data);
                if (data.sucesso) {
                    $("#aguarde").hide();
                    $("#redirecting").show();
                    url = data.content.url;
                    iniciaContador();
                    setTimeout('window.location = url;', 5000);
                }
                else {
                    exibeMensagemErro(data.content["L_ERRORCODE0"], data.content["L_SHORTMESSAGE0"] + " - " + data.content["L_LONGMESSAGE0"]);
                }
            });
    }

    $(".msg-danger").on("click", ".pagar", function() {
        enviaPagamento();
    });

    $(".msg-success").on("click", ".ir-mp", function() {
        window.location = url;
    });

    function exibeMensagemErro(status, mensagem) {
        $payPalMensagem.find(".msg-warning").hide();
        $payPalMensagem.toggleClass("alert-message-warning alert-message-danger");
        var $errorMessage = $("#errorMessage");
        $errorMessage.text(status + ": " + mensagem);
        $payPalMensagem.find(".msg-danger").show();
    }

    function exibeMensagemSucesso(situacao) {
        $payPalMensagem.find(".msg-warning").hide();
        $payPalMensagem.toggleClass("alert-message-warning alert-message-success");
        var $success = $payPalMensagem.find(".msg-success");
        $success.find("#redirecting").hide();
        if (situacao == "pago") {
            $success.find("#successMessage").show();
        }
        else {
            $success.find("#pendingMessage").show();
        }
        $success.show();
    }

    var pedidoPago = '{{ pedido.situacao_id }}' == '4';
    var pedidoAguardandoPagamento = '{{ pedido.situacao_id }}' == '2';

    if (window.location.search != "" && window.location.search.indexOf("failure") > -1) {
        exibeMensagemErro(500, "Pagamento cancelado no MercadoPago!");
    }
    else if (window.location.search != "" && window.location.search.indexOf("success") > -1 || pedidoPago) {
        exibeMensagemSucesso("pago");
    }
    else if (window.location.search != "" && window.location.search.indexOf("pending") > -1 || pedidoAguardandoPagamento) {
        exibeMensagemSucesso("aguardando");
    }
    else {
        enviaPagamento();
    }
});
