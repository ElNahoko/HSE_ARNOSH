# -*- coding: utf-8 -*-
from odoo import http

# class Accident(http.Controller):
#     @http.route('/accident/accident/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accident/accident/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accident.listing', {
#             'root': '/accident/accident',
#             'objects': http.request.env['accident.accident'].search([]),
#         })

#     @http.route('/accident/accident/objects/<model("accident.accident"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accident.object', {
#             'object': obj
#         })