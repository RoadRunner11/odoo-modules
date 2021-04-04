# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.modules.module import get_module_resource
import pysftp
import logging
import csv
import time
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
	# monkey.patch_all()
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None

	myHostname = "sftpnordic.staples-solutions.com"
	myUsername = "P4734998"
	myPassword = "54dLohN3"
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
		# path = get_module_resource('inventory_updates', 'static/src/')
		module_path = get_module_resource('inventory_updates', 'static/src/')
		remoteFilePaths = ['Price/prisfil.csv', 'Price/varefil.csv', 'Beholdning/beholdning300.csv']

		localFilePaths = ['prisfil.csv', 'varefil.csv', 'beholdning300.csv']
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
	producer = fields.Char('Producer')
	prod_type = fields.Char('Product Type')
	group1 = fields.Char('Group 1')
	group2 = fields.Char('Group 2')
	group3 = fields.Char('Group 3')
	ipakn = fields.Char('IPAKN')
	ypakk = fields.Char('YPAKK')
	limit = fields.Char('LIMIT')
	originr = fields.Char('ORIGINR')
	price_per = fields.Char('PRICE PER')
	imagelink =  fields.Char('IMAGE LINK')

	@api.model
	def create_product_data(self):
		move_files()
		module_path = get_module_resource('inventory_updates', 'static/src/')
		prisfil_path = module_path + 'prisfil.csv'
		varefil_path = module_path + 'varefil.csv'
		beholding_path = module_path + 'beholdning300.csv'
		with open(prisfil_path, 'r') as prisfil, open(varefil_path, 'r') as varefil, open(beholding_path, 'r') as beholding:
			prisfil_data = csv.reader(prisfil, escapechar= '\t')
			varefil_data = csv.reader(varefil)
			beholdinfg_data = csv.reader(beholding)
			next(prisfil_data)
			next(varefil_data)
			next(beholdinfg_data)
			count1 = 0
			count2 = 0
			for row in varefil_data:
				if count1 >=10 :
					break
				data = {}
				row = ''.join(row).split(';')
				data['type'] = 'product'
				data['default_code'] = row[1]
				data['name'] = row[2]
				data['ipakn'] = row[3]
				data['price_per'] = row[4]
				data['originr'] = row[5]
				data['producer'] = row[6]
				data['prod_type'] = row[9]
				data['limit'] = row[11]
				data['ypakk'] = row[12]
				data['group1'] = row[14]
				data['group2'] = row[15]
				data['group3'] = row[16]
				data['description'] = row[17]
				data['imagelink'] = row[27]
				duplicates = self.search([('default_code', '=', data['default_code'])])
				if duplicates:
					for product in duplicates:
						product.write(data)
				else:
					self.env['product.template'].create(data)
				count1 += 1

			for row in prisfil_data:
				if count2 >=10 :
					break
				default_code = row[0][7:12]
				duplicates = self.search([('default_code', '=', default_code)])
				if duplicates:
					for product in duplicates:
						product.write({'price': float(row[1])})
				count2 += 1

			for row in beholdinfg_data:
				if count3 >=10 :
					break
				row = ''.join(row).split(';')
				default_code = row[0]
				duplicates = self.search([('default_code', '=', default_code)])
				if duplicates:
					for product in duplicates:
						product.write({'qty_available': float(row[1])})
				count2 += 1
				
		_logger.info('Done')
		return {}

	@api.model
	def run_scheduler(self):
		for _ in range(5):
			_logger.info('testing this out')
		return {}