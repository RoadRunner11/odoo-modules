odoo.define('payment_yoco.payment_form', function (require) {
    "use strict";
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var PaymentForm = require('payment.payment_form');

    var qweb = core.qweb;
    var _t = core._t;

    
    PaymentForm.include({

        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return ajax.loadJS("https://js.stripe.com/v3/");
            })
        },

    })    

})