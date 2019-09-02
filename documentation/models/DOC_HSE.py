# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DOCHSE(models.Model):
    _name = 'document'
    _rec_name = 'categorie'

    categorie = fields.Many2one(
        'document.categorie',
        string="Catégorie",
        required=False, )
    description = fields.Char(
        string="Description")
    Document_binaire = fields.Binary(
        string="Fichier",)
    Nom_Document = fields.Char(
        string="Filename",
        required=False, )

    @api.multi
    def print_doc(self):
        return self.env.ref('documentation.action_report_doc').report_action(self)

class DOCUMENTCATEGORIE(models.Model):
    _name = 'document.categorie'
    _rec_name = 'categorie'

    categorie = fields.Char(
        string="catégorie",
        required=False, )
    date = fields.Datetime(
        string="Date",
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True,
        required=False, )

