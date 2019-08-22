# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DOCHSE(models.Model):
    _name = 'document'
    _rec_name = 'Document_binaire'

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

class DOCUMENTCATEGORIE(models.Model):
    _name = 'document.categorie'
    _rec_name = 'categorie'

    categorie = fields.Char(
        string="catégorie",
        required=False, )

