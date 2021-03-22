# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryUpdates(http.Controller):
#     @http.route('/inventory_updates/inventory_updates/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_updates/inventory_updates/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_updates.listing', {
#             'root': '/inventory_updates/inventory_updates',
#             'objects': http.request.env['inventory_updates.inventory_updates'].search([]),
#         })

#     @http.route('/inventory_updates/inventory_updates/objects/<model("inventory_updates.inventory_updates"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_updates.object', {
#             'object': obj
#         })
