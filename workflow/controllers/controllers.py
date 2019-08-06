# -*- coding: utf-8 -*-
from odoo import http

# class Workflow(http.Controller):
#     @http.route('/workflow/workflow/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/workflow/workflow/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('workflow.listing', {
#             'root': '/workflow/workflow',
#             'objects': http.request.env['workflow.workflow'].search([]),
#         })

#     @http.route('/workflow/workflow/objects/<model("workflow.workflow"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('workflow.object', {
#             'object': obj
#         })