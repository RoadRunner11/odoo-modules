# -*- coding: utf-8 -*-
# from odoo import http


# class HospitalTreatmentPlans(http.Controller):
#     @http.route('/hospital_treatment_plans/hospital_treatment_plans/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospital_treatment_plans/hospital_treatment_plans/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospital_treatment_plans.listing', {
#             'root': '/hospital_treatment_plans/hospital_treatment_plans',
#             'objects': http.request.env['hospital_treatment_plans.hospital_treatment_plans'].search([]),
#         })

#     @http.route('/hospital_treatment_plans/hospital_treatment_plans/objects/<model("hospital_treatment_plans.hospital_treatment_plans"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospital_treatment_plans.object', {
#             'object': obj
#         })
