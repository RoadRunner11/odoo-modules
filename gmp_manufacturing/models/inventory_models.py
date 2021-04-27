# -*- coding: utf-8 -*-

import xlrd
import tempfile
import binascii

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Requisition(models.Model):
    _name = 'manufacturing.requisition'
    _description = "Requisition"
    
    name = fields.Char('Requisition #', index=True, required=True, translate=True)
    vendor_id = fields.Many2one(
        'res.partner', 'Vendor',
        ondelete='cascade', required=True)
    show_only_this_vendors_materials = fields.Boolean()
    associate_with_project = fields.Many2one("manufacturing.project")
    po_no = fields.Integer("PO #")
    order_by = fields.Date()
    needed_by = fields.Date()
    comment = fields.Text()
    material_requisition = fields.Many2many(comodel_name="manufacturing.mat.req")
    requested_by = fields.Many2one('res.users')
    
    @api.model
    def create (self, vals):
        vals["name"] = str(len(self.env["manufacturing.requisition"].search([])) + 1)

        return super(Requisition, self).create(vals)


class MaterialRequisition(models.Model):
    _name = 'manufacturing.mat.req'
    _description = "Material Requisition"
    
    name = fields.Char('Material Requisition #', index=True, translate=True)
    part_no = fields.Integer("Part #")
    material_name = fields.Char()
    material_id = fields.Char("Material Id")
    version = fields.Integer()
    material_uom_id = fields.Many2one('uom.uom', 'Material Unit')
    vendor_part_no = fields.Integer("Vendor Part #")
    vendor_catalog_no = fields.Integer("Vendor Catalog #")
    cost_per_unit = fields.Float('Cost/Unit', default=0.000000, digits='Product Price')
    quantity = fields.Float()
    uom_id = fields.Many2one('uom.uom', 'Unit')
    msds = fields.Boolean("MSDS")
    c_of_a = fields.Boolean("C of A")
    
    @api.model
    def create (self, vals):
        vals["name"] = str(len(self.env["manufacturing.mat.req"].search([])) + 1)

        return super(MaterialRequisition, self).create(vals)

    @api.onchange('part_no')
    def part_no_onchange(self):
        if self.part_no:
            material = self.env['manufacturing.material'].search(
                [('part_no', '=', self.part_no)], limit=1)
            if material:
                self.material_name = material.name
                self.material_id = material.material_id
                self.material_uom_id = material.uom_id
                self.cost_per_unit = material.cost_per_unit
            else: raise UserError(
                    _("There is no material with this part number"))


class PendingReceipt(models.Model):
    _name = 'manufacturing.pending.receipt'
    
    name = fields.Char('Receipt #', index=True, required=True, translate=True)
    part_no = fields.Integer("Part #")
    material_name = fields.Char()
    material_id = fields.Char("Material Id")
    version = fields.Char()
    vendor_name = fields.Char()
    vendor_part_no = fields.Integer("Vendor Part #")
    project = fields.Char()
    requisition_no = fields.Integer("Requisition #")
    po_no = fields.Integer("PO #")
    qty_ord = fields.Float()
    qty_rcv = fields.Float()
    uom_id = fields.Many2one('uom.uom', 'Unit')
    receipt_upload = fields.Binary()
    upload_receipt_file_name = fields.Char()

    @api.model
    def create (self, vals):
        vals["name"] = str(len(self.env["manufacturing.pending.receipt"].search([])) + 1)

        return super(PendingReceipt, self).create(vals)

    @api.onchange('receipt_upload')
    def upload_receipt_upload_onchange(self):
        if self.receipt_upload:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.receipt_upload))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    line = [col.decode() if type(col) != str else col for col in line] # Make the line a list of string column values

                    part_no = int(float(line[1]))
                    material = self.env['manufacturing.material'].search(
                        [('part_no', '=', part_no)], limit=1)
                    if not material:
                        raise UserError(
                            _("There is no material with this part number: " + str(part_no)))

                    requisition_no = int(float(line[0]))
                    req = self.env['manufacturing.requisition'].search(
                        [('name', '=', str(requisition_no))], limit=1)
                    if not req:
                        raise UserError(
                            _("There is no requisition with this number: " + str(requisition_no)))

                    mat_req = req.material_requisition.search(
                        [('part_no', '=', part_no)], limit=1)
                    if not req:
                        raise UserError(
                            _("There is no material requisition with this part number: " + str(part_no)))

                    print("=========", part_no, requisition_no, mat_req.name)
                    
                    self.part_no = part_no
                    self.material_name = material.name
                    self.material_id = material.material_id
                    self.version = line[2]
                    self.vendor_name = req.vendor_id.name
                    self.requisition_no = requisition_no
                    self.po_no = int(float(line[11]))
                    self.qty_ord = mat_req.quantity
                    self.qty_rcv = float(line[4])

                    self.env['manufacturing.inventory'].create({
                        "name": material.name,
                        "part_no": part_no,
                        "qty_remain": float(line[4]),
                        "qty_rcv": float(line[4]),
                        "material_id": material.material_id,
                        "requisition_no": int(float(requisition_no)),
                        "po_no": int(float(line[11]))
                    })

                    # print ("==========", [col.decode() if type(col) != str else col for col in line])  # in this line variable you get the value line by line from excel.


class InventoryManagement(models.Model):
    _name = 'manufacturing.inventory'
    
    name = fields.Char('Material Name')
    part_no = fields.Integer("Part #")
    qty_remain = fields.Float()
    receipt_no = fields.Integer("Receipt #")
    vendor_name = fields.Char()
    qty_rcv = fields.Float()
    material_id = fields.Char("Material Id")
    requisition_no = fields.Integer("Requisition #")
    po_no = fields.Integer("PO #")
    product_name = fields.Char()