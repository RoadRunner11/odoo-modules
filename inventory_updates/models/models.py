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
import requests
import base64


class CustomImage():
	def load_image_from_url(self, url):
		data = ''

		try:
			# Python 2
			# data = requests.get(url.strip()).content.encode('base64').replace('\n', '')

			# Python 3
			data = base64.b64encode(requests.get(url.strip()).content).replace(b'\n', b'')
		except Exception as e:
			_logger.warn('There was a problem requesting the image from URL %s' % url)
			logging.exception(e)

		return data

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

class ProductCategory(models.Model, CustomImage):
	_name = "product.category"
	_inherit = "product.category"
	group_type = fields.Selection([
        ('group1', 'Group 1'),
        ('group2', 'Group 2'), 
		('group3', 'Group 3')], string='Group Type', default='group3', required=True,
        )
	group_id = fields.Char('Group Id')

class ProductTemplate(models.Model, CustomImage):
	_name = "product.template"
	_inherit = "product.template"

	_sql_constraints = [
		('name_uniq', 'unique (internal_id)', "Product ID already exists !"),
	]
	certifications_id = fields.Many2many(
		'inventory_updates.certifications', 'Certifications', help="Product certifications")
	producer = fields.Char('Producer')
	prod_type = fields.Char('Product Type')
	# group1 = fields.Many2one('product.category', 'Parent Category', index=True, ondelete='cascade')
	# group2 = fields.Many2one('product.category', 'Parent Category', index=True, ondelete='cascade')
	# group3 = fields.Many2one('product.category', 'Parent Category', index=True, ondelete='cascade')
	ipakn = fields.Char('IPAKN')
	ipakk = fields.Char('IPAKK')
	ypakk = fields.Char('YPAKK')
	pall = fields.Char('PALL')
	# limit = fields.Char('LIMIT')
	originr = fields.Char('ORIGINR')
	price_per = fields.Char('PRICE PER')
	imagelink =  fields.Char('IMAGE LINK')
	miljo1 = fields.Char('Miljo One')
	miljo2 = fields.Char('Miljo Two')
	miljo3 = fields.Char('Miljo Three')
	miljo4 = fields.Char('Miljo Four')
	miljo5 = fields.Char('Miljo Five')
	# image = fields.Binary(string='Image', store=True, attachment=False)

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
			# next(beholdinfg_data)
			count1 = 0
			count2 = 0
			count3 = 0
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
				data['ipakk'] = row[12]
				data['ypakk'] = row[13]
				data['pall'] = row[14]
				data['description'] = row[19]
				data['imagelink'] = row[27]
				data['price'] = float(0)
				data['miljo1'] = row[21]
				data['miljo2'] = row[22]
				data['miljo3'] = row[23]
				data['miljo4'] = row[24]
				data['miljo5'] = row[25]
				if data['imagelink']:
					image = self.load_image_from_url(data['imagelink'])
					data['image_1920'] = image
				if row[18]:
					group3_id = self.env['product.category'].search([('name', '=', row[18])])
					if group3_id:
						data['categ_id'] = group3_id
					# data['group1'] = group3_id.parent_id.parent_id
					# data['group2'] = group3_id.parent_id
					# data['group3'] = group3_id

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
				row = ''.join(row[0]).split(';')
				default_code = row[1]
				duplicates = self.search([('default_code', '=', default_code)])
				if duplicates:
					for product in duplicates:
						product.write({'standard_price': float(row[2])})
				count2 += 1

			for row in beholdinfg_data:
				if count3 >=10 :
					break
				row = ''.join(row).split(';')
				product_id = 0
				template_id = 0
				default_code = row[0]
				product = self.env['product.product'].search([('default_code', '=', default_code)])
				product_t = self.search([('default_code', '=', default_code)])
				if product:
					product_id = product.id 
				if product_t:
					template_id = product_t.id 
				if product_id and template_id:
					data = {'product_id':product_id, 'product_tmpl_id':template_id, 'new_quantity':abs(float(row[1]))}
					change_qty = self.env['stock.change.product.qty']
					move = self.env['stock.move']
					p_move = move.search([('product_id', '=', product_id)])
					if p_move:
						# _logger.info('found {}'.format(product_id))
						p_move.write({'product_uom_qty':abs(float(row[1]))})
					else:
						# _logger.info('not found {}'.format(product_id))
						new_qty = change_qty.create(data)
						new_qty.change_product_qty()
					
				count3 += 1
				
		_logger.info('Done')
		return {}

	@api.model
	def run_scheduler(self):
		for _ in range(5):
			_logger.info('testing this out')
		return {}

	# @api.multi
	# @api.depends('imagelink')
	# def _compute_image(self):
	# 	for record in self:
	# 		image = None
	# 		if record.imagelink:
	# 			image = self.load_image_from_url(record.imagelink)
	# 		record.update({'image': image, })