# -*- coding: utf-8 -*-
from odoo import http

# class GMateriel(http.Controller):
#     @http.route('/g__materiel/g__materiel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g__materiel/g__materiel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('g__materiel.listing', {
#             'root': '/g__materiel/g__materiel',
#             'objects': http.request.env['g__materiel.g__materiel'].search([]),
#         })

#     @http.route('/g__materiel/g__materiel/objects/<model("g__materiel.g__materiel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g__materiel.object', {
#             'object': obj
#         })