# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Material(models.Model):
    _name = 'manufacturing.material'
    _description = "Material"
    _sql_constraints = [
        ('part_no_unique', 'unique(part_no)',
         'Another material has this part number already!'),
    ]
    
    categ_id = fields.Many2one('product.category', 'Type (Category)', required=True)
    material_type = fields.Selection([
        ('raw', 'Raw Material'),
        ('finished', 'Finished Good'),
    ], default='raw')
    part_no = fields.Integer("Part #", readonly=True, unique=True)
    name = fields.Char('Material Name', index=True, required=True, translate=True)
    description = fields.Text('Material Description', translate=True)
    uom_id = fields.Many2one('uom.uom', 'Unit', required=True)
    thc_level = fields.Float("THC Level (%)", digits=(3,4))
    cbd_level = fields.Float("CBD Level (%)", digits=(3,4))
    material_id = fields.Char("Material Id")
    cost_per_unit = fields.Float('Cost/Unit', default=0.000000, digits='Product Price')
    default_alert_level_quantity = fields.Float()
    default_reorder_level_quantity = fields.Float()
    default_order_lead_time = fields.Integer("Default Order Lead Time (days)")
    account = fields.Char()
    storage_condition = fields.Many2one("manufacturing.storage", required=True)
    recommended_shelf_life = fields.Char()
    retest_period = fields.Float("QM Retest Period (months)")
    expiry_period = fields.Float("Expiry Period (months)")

    @api.model
    def create (self, vals):
        vals["part_no"] = len(self.env["manufacturing.material"].search([])) + 1

        return super(Material, self).create(vals)


class StorageCondition(models.Model):
    _name = "manufacturing.storage"
    _description = "Storage Condition"

    name = fields.Char("Storage Condition")


class Specification(models.Model):
    _name = 'manufacturing.specification'
    _description = "Specification"
    
    name = fields.Char('Specification Number', index=True, required=True, translate=True)
    material = fields.Many2one('manufacturing.material', 'Material', required=True)
    material_id = fields.Char(related="material.material_id")
    part_no = fields.Integer("Part #", readonly=True, related="material.part_no")
    spec_version = fields.Integer("Specification Version #", default=1)
    effective_date = fields.Date()
    retest_period = fields.Float("QM Retest Period (months)")
    expiry_period = fields.Float("Expiry Period (months)")
    safety_instructions = fields.Text("Safety and Handling Instructions")
    general_sampling = fields.Text("General Sampling")
    attachment = fields.Binary()
    attached_file = fields.Char()
    tests = fields.Many2many(comodel_name="manufacturing.spec.test")

    @api.model
    def create (self, vals):
        vals["name"] = str(len(self.env["manufacturing.specification"].search([])) + 1)

        return super(Specification, self).create(vals)


class Test(models.Model):
    _name = "manufacturing.spec.test"
    _description = "Test"

    name = fields.Char("Test")