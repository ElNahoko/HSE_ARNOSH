# -*- coding: utf-8 -*-
from odoo import http

# class Reunion(http.Controller):
#     @http.route('/reunion/reunion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reunion/reunion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reunion.listing', {
#             'root': '/reunion/reunion',
#             'objects': http.request.env['reunion.reunion'].search([]),
#         })

#     @http.route('/reunion/reunion/objects/<model("reunion.reunion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reunion.object', {
#             'object': obj
#         })