# -*- coding: utf-8 -*-
from odoo import http

# class ControleEquipement(http.Controller):
#     @http.route('/controle_equipement/controle_equipement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/controle_equipement/controle_equipement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('controle_equipement.listing', {
#             'root': '/controle_equipement/controle_equipement',
#             'objects': http.request.env['controle_equipement.controle_equipement'].search([]),
#         })

#     @http.route('/controle_equipement/controle_equipement/objects/<model("controle_equipement.controle_equipement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('controle_equipement.object', {
#             'object': obj
#         })