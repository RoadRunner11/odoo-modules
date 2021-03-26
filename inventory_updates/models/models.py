# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
import pysftp
import logging
import csv
import shutil
from gevent import monkey

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
def move_files():
    monkey.patch_all()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    myHostname = "sftpnordic.staples-solutions.com"
    myUsername = "P4734998"
    myPassword = "54dLohN3"
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
        # path = get_module_resource('inventory_updates', 'static/src/')
        module_path = '/home/fodilu/odoo13/custom/addons/inventory_updates/static/src/'
        remoteFilePaths = ['Price/prisfil.csv', 'Price/varefil.csv']

        localFilePaths = ['prisfil.csv', 'varefil.csv']
        for loc, remote_path in enumerate(remoteFilePaths):
            file_instance = sftp.open(remote_path, 'r')
            with open(module_path + localFilePaths[loc], 'wb') as out_file:
                shutil.copyfileobj(file_instance, out_file)

class Certification(models.Model):
    _name = 'inventory_updates.certifications'
    _description = 'inventory certifications'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    image = fields.Binary()


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    _sql_constraints = [
        ('name_uniq', 'unique (internal_id)', "Product ID already exists !"),
    ]
    certifications_id = fields.Many2many(
        'inventory_updates.certifications', 'Certifications', help="Product certifications")
    internal_id = fields.Char('Internal ID')
    producer = fields.Char('Producer')
    barcode = fields.Char('Barcode')
    group1 = fields.Char('Group 1')
    group2 = fields.Char('Group 2')
    group3 = fields.Char('Group 3')

    def create_product_data(self):
        move_files()
        module_path = get_module_resource('inventory_updates', 'static/src/')
        prisfil_path = module_path + 'prisfil.csv'
        varefil_path = module_path + 'varefil.csv'
        with open(prisfil_path, 'r') as prisfil, open(varefil_path, 'r') as varefil:
            prisfil_data = csv.reader(prisfil, escapechar= '\t')
            varefil_data = csv.reader(varefil)
            count = 0
            for row in varefil_data:
                if count >=10 :
                    break
                data = {}
                row = ''.join(row).split(';')
                data['internal_id'] = row[1]
                data['name'] = row[2]
                data['producer'] = row[6]
                data['barcode'] = row[9]
                data['group1'] = row[14]
                data['group2'] = row[15]
                data['group3'] = row[16]
                data['description'] = row[17]
                duplicates = self.search([('internal_id', '=', data['internal_id'])])
                if duplicates:
                    for product in duplicates:
                        product.write(data)
                else:
                    self.env['product.template'].create(data)
                count += 1
        _logger.info('Done')