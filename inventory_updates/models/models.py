# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
import logging

_logger = logging.getLogger(__name__)

# class inventory_updates(models.Model):
#     _name = 'inventory_updates.inventory_updates'
#     _description = 'inventory_updates.inventory_updates'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class Certification(models.Model):
    _name = 'inventory_updates.certifications'
    _description = 'inventory certifications'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    image = fields.Binary()


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"
    
    certifications_id = fields.Many2many(
        'inventory_updates.certifications', 'Certifications', help="Product certifications")
    producer = fields.Char('Producer')

    def create_product_data(self):
        _logger.info("hello there")
    