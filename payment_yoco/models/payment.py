# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import requests
import pprint
import json

from hashlib import md5
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
# from odoo.addons.payment_alipay.controllers.main import AlipayController
from odoo.http import request
from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class PaymentAcquirerYoco(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('yoco', 'Yoco')])#, ondelete={'yoco': 'set default'})
    # yoco_merchant_id = fields.Char(string="Yoco Merchant ID", required_if_provider='yoco', groups='base.group_user')
    yoco_pub_key = fields.Char(string="Yoco Pub Key", required_if_provider='yoco', groups='base.group_user')
    yoco_sec_key = fields.Char(string="Yoco Sec Key", required_if_provider='yoco', groups='base.group_user')

    def _get_yoco_api_url(self):
        """ PayUlatam URLs"""
        return 'https://online.yoco.com/v1/charges/'
    

class PaymentTransactionYoco(models.Model):
    _inherit = 'payment.transaction'

    def _yoco_verify_charge(self, data):
        api_url_charge =  self.acquirer_id._get_yoco_api_url()
        sec_key = request.env['payment.acquirer'].browse(data['acquirer_id']).yoco_sec_key
        payload = {
            'token': data['token'],
            'amountInCents': data['amount'],
            'currency': data['currency']
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Secret-Key': sec_key
        }
        _logger.info('_yoco_verify_charge: Sending values to URL %s, values:\n%s \n with sec_key %s', api_url_charge, pprint.pformat(payload), sec_key)
        r = requests.post(api_url_charge,headers=headers, data=json.dumps(payload))
        # res = r.json()
        _logger.info('_rave_verify_charge: Values received:\n%s', pprint.pformat(r))
        return self._yoco_validate_tree(r.json(),data)

    def _yoco_validate_tree(self, tree, data):
        self.ensure_one()
        if self.state != 'draft':
            _logger.info('Rave: trying to validate an already validated tx (ref %s)', self.reference)
            return True

        status = tree.get('status')
        amount = tree["amountInCents"]
        currency = tree["currency"]
        
        if status == 'successful' and amount == data["amount"] and currency == data["currency"] :
            self.write({
                'date': fields.datetime.now(),
                'acquirer_reference': tree["id"],
            })
            self._set_transaction_done()
            self.execute_callback()
            if self.payment_token_id:
                self.payment_token_id.verified = True
            return True
        else:
            error = tree['errorMessage']
            _logger.warn(error)
            self.sudo().write({
                'state_message': error,
                'acquirer_reference':tree["id"],
                'date': fields.datetime.now(),
            })
            self._set_transaction_cancel()
            return False
