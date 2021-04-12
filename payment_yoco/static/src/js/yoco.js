odoo.define('payment_stripe.stripe', function (require) {
    "use strict";
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    
    var qweb = core.qweb;
    var _t = core._t;

    ajax.loadXML('/payment_yoco/static/src/xml/yoco_templates.xml', qweb);
    
    if ($.blockUI) {
        // our message needs to appear above the modal dialog
        $.blockUI.defaults.baseZ = 2147483647; //same z-index as Rave Checkout
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    function payWithYoco(acquirer_id , pubKey,email,amount,phone,currency,invoice_num) {
        console.log(acquirer_id , pubKey,email,amount,phone,currency,invoice_num)
        
        var yoco = new window.YocoSDK({
            publicKey: pubKey,
            });
        
        yoco.showPopup({
            amountInCents: amount,
            currency: 'ZAR',
            name: 'Your Store or Product',
            description: 'Awesome description',
            callback: function (result) {
                // This function returns a token that your server can use to capture a payment
                if (result.error) {
                const errorMessage = result.error.message;
                alert("error occured: " + errorMessage);
                } else {
                    // if ($.blockUI) {
                    //     var msg = _t("Just one more second, confirming your payment...");
                    //     $.blockUI({
                    //         'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                    //                 '    <br />' + msg +
                    //                 '</h2>'
                    //     });
                    // }
                    if ( result.status == "charge_ready") {
                        // redirect to a success page
                        ajax.jsonRpc("/payment/yoco/verify_charge", 'call', {
                            token : result.id,
                            acquirer_id: acquirer_id,
                            amount: amount,
                            currency: currency,
                            tx_ref:invoice_num
                        }).then(function(data){
                            //console.log(data);
                            window.location.href = data;
                        }).catch(function(data){
                            console.log("Failed to redirect!");
                            var msg = data && data.data && data.data.message;
                            var wizard = $(qweb.render('yoco.error', {'msg': msg || _t('Payment error')}));
                            wizard.appendTo($('body')).modal({'keyboard': true});
                        });
                    }    
                    
                }
                // In a real integration - you would now pass this chargeToken back to your
                // server along with the order/basket that the customer has purchased.
            }
        })
        if ($.blockUI) {
            $.unblockUI();
        }
        $("#o_payment_form_pay").removeAttr('disabled');
    }
    

    var observer = new MutationObserver(function (mutations, observer) {
        for (var i = 0; i < mutations.length; ++i) {
            for (var j = 0; j < mutations[i].addedNodes.length; ++j) {
                console.log(mutations[i].addedNodes)
                console.log(mutations[i].addedNodes.length)
                console.log(mutations[i].addedNodes.tagName)
                // display_yoco_form($(mutations[i].addedNodes[j]));
                if (mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') === 'yoco') {
                    display_yoco_form($(mutations[i].addedNodes[j]));
                }
            }
        }
    });
    
    function displayError(message) {
        var wizard = $(qweb.render('yoco.error', {'msg': message || _t('Payment error')}));
        wizard.appendTo($('body')).modal({'keyboard': true});
        if ($.blockUI) {
            $.unblockUI();
        }
        $("#o_payment_form_pay").removeAttr('disabled');
    }
    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return Promise.reject("DOM doesn't contain '.o_payment_form'");
    }else{
        function display_yoco_form(provider_form){
            // Open Checkout with further options
            // if ($.blockUI) {
            //     var msg = _t("Just one more second, We are redirecting you to Yoco...");
            //     $.blockUI({
            //         'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
            //                 '    <br />' + msg +
            //                 '</h2>'
            //     });
            // }
            // var paymentForm = $('.o_payment_form');
            // if (!paymentForm.find('i').length) {
            //     paymentForm.append('<i class="fa fa-spinner fa-spin"/>');
            //     paymentForm.attr('disabled', 'disabled');
            //     console.log("there is paymentForm")
            // }
    
            var get_input_value = function (name) {
                return provider_form.find('input[name="' + name + '"]').val();
            };
            console.log(get_input_value('yoco_pub_key'))
    
            ajax.jsonRpc("/payment/yoco/values", 'call', {
                acquirer_id : parseInt(provider_form.find('#acquirer_yoco').val()),
                amount : parseFloat(get_input_value("amount") || '0.0') * 17 * 100,
                currency : 'ZAR',//get_input_value("currency"),
                email : get_input_value("email"),
                name : get_input_value("name"),
                publicKey : get_input_value("yoco_pub_key"),
                invoice_num : get_input_value("invoice_num"),
                phone : get_input_value("phone"),
                return_url :   get_input_value("return_url"),
                merchant :  get_input_value("merchant")
            }).then(function(data){
                // displayError("testing if error will show")

                payWithYoco(data.acquirer_id, data.publicKey, data.email, data.amount, data.phone, data.currency, data.invoice_num);
            }).catch(function(data){
                console.log("Failed!");
                var msg = data && data.data && data.data.message;
                var wizard = $(qweb.render('yoco.error', {'msg': msg || _t('Payment error')}));
                wizard.appendTo($('body')).modal({'keyboard': true});
            });
            
        }
    
        $.getScript("https://js.yoco.com/sdk/v1/yoco-sdk-web.js", function(data, textStatus, jqxhr) {
            // observer.observe(document.body, {childList: true});
            display_yoco_form($('form[provider="yoco"]'));
        });
    }
    
})