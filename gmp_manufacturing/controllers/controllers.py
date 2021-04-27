# -*- coding: utf-8 -*-
# from odoo import http


# class ShippingPartners(http.Controller):
#     @http.route('/shipping_partners/shipping_partners/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shipping_partners/shipping_partners/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shipping_partners.listing', {
#             'root': '/shipping_partners/shipping_partners',
#             'objects': http.request.env['shipping_partners.shipping_partners'].search([]),
#         })

#     @http.route('/shipping_partners/shipping_partners/objects/<model("shipping_partners.shipping_partners"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shipping_partners.object', {
#             'object': obj
#         })
