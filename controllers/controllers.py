# -*- coding: utf-8 -*-
from odoo import http

# class Emsi(http.Controller):
#     @http.route('/emsi/emsi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emsi/emsi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emsi.listing', {
#             'root': '/emsi/emsi',
#             'objects': http.request.env['emsi.emsi'].search([]),
#         })

#     @http.route('/emsi/emsi/objects/<model("emsi.emsi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emsi.object', {
#             'object': obj
#         })