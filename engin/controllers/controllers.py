# -*- coding: utf-8 -*-
from odoo import http

# class Engin(http.Controller):
#     @http.route('/engin/engin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engin/engin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('engin.listing', {
#             'root': '/engin/engin',
#             'objects': http.request.env['engin.engin'].search([]),
#         })

#     @http.route('/engin/engin/objects/<model("engin.engin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engin.object', {
#             'object': obj
#         })