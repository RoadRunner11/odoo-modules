# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Project(models.Model):
    _name = "manufacturing.project"
    _description = "Project"

    name = fields.Char("Project Title")
    description = fields.Text()
    wip_fg_part_no = fields.Many2many("manufacturing.wip_fg_part_no", string="WIP/FG Part #")
    material_ids = fields.Many2many("manufacturing.material", string="Materials")
    client_ids = fields.Many2many('res.partner', string='Clients')
    personnel_ids = fields.Many2many('res.users', string='Personnel')


class Project(models.Model):
    _name = "manufacturing.wip_fg_part_no"
    _description = "WIP/FG Part #"

    part_no = fields.Integer("Part #")
    material_name = fields.Char()
    version = fields.Char()
    strength = fields.Char()
    suffix = fields.Char()
    primary_container = fields.Char()

    @api.onchange('part_no')
    def part_no_onchange(self):
        if self.part_no:
            material = self.env['manufacturing.material'].search(
                [('part_no', '=', self.part_no)], limit=1)
            if material:
                self.material_name = material.name
            else: raise UserError(
                    _("There is no material with this part number"))
