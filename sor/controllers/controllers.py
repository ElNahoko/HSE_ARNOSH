# -*- coding: utf-8 -*-
from odoo import http

# class Sor(http.Controller):
#     @http.route('/sor/sor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sor/sor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sor.listing', {
#             'root': '/sor/sor',
#             'objects': http.request.env['sor.sor'].search([]),
#         })

#     @http.route('/sor/sor/objects/<model("sor.sor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sor.object', {
#             'object': obj
#         })