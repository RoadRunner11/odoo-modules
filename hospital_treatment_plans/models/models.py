# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hospital_treatment_plans(models.Model):
#     _name = 'hospital_treatment_plans.hospital_treatment_plans'
#     _description = 'hospital_treatment_plans.hospital_treatment_plans'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
