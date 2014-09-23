//{% load filters %}
var url = '';
var $counter = null;
var segundos = 5;
$(function() {
    var $depositoMensagem = $(".deposito-mensagem");

    function enviaPagamento() {
        $depositoMensagem.find(".msg-danger").hide();
        $depositoMensagem.find(".msg-success").hide();
        $depositoMensagem.find(".msg-warning").show();
        $depositoMensagem.removeClass("alert-message-success");
        $depositoMensagem.removeClass("alert-message-danger");
        $depositoMensagem.addClass("alert-message-warning");
        var url_pagar = '{% url_loja "checkout_pagador" pedido.numero pagamento.id %}';
        $.getJSON(url_pagar)
            .fail(function (data) {
                exibeMensagemErro(data.status, data.content);
            })
            .done(function (data) {
                console.log(data);
                if (data.sucesso) {
                    $("#aguarde").hide();
                    exibeMensagemSucesso()
                }
                else {
                    exibeMensagemErro(data.status, data.content);
                }
            });
    }

    function exibeMensagemErro(status, mensagem) {
        $depositoMensagem.find(".msg-warning").hide();
        $depositoMensagem.toggleClass("alert-message-warning alert-message-danger");
        var $errorMessage = $("#errorMessage");
        $errorMessage.text(status + ": " + mensagem);
        $depositoMensagem.find(".msg-danger").show();
    }

    function exibeMensagemSucesso() {
        $depositoMensagem.find(".msg-warning").hide();
        $depositoMensagem.toggleClass("alert-message-warning alert-message-success");
        var $success = $depositoMensagem.find(".msg-success");
        $success.find("#successMessage").show();
        $success.show();
    }

    $(".msg-danger").on("click", ".pagar", function() {
        enviaPagamento();
    });

    var pedidoPago = '{{ pedido.situacao_id }}' == '4';

    if (pedidoPago) {
        exibeMensagemSucesso("pago");
    }
    else {
        enviaPagamento();
    }
});
