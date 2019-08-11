# -*- coding: utf-8 -*-

from odoo import models, fields, api

class regle(models.Model):
    _name = 'reg.reg'
    _rec_name = 'nom'

    nom = fields.Char(
        string="Règle",
        required=False, )
    
    icon = fields.Binary(
        string="Icone",  )
    
    desc = fields.Char(
        string="Description"
        , required=False, )

class gravite(models.Model):
    _name = 'gra.gra'
    _rec_name = 'grav'

    grav = fields.Char(
        string="Gravité",
        required=False, )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      


class accident(models.Model):
    _name = 'acc.acc'
    _rec_name = 'type'

    type = fields.Selection(
        string="Type",
        selection=[('Accident', 'Accident'),
                   ('Incident', 'Incident'), ],
        required=False, )
    
    gravite = fields.Many2one(
        'gra.gra',
        string="Gravité",
        required=False, )
    
    regle = fields.Many2one(
        'reg.reg',
        string="Règle de sécurité",
        required=False, )
    
    date = fields.Datetime(
        string="Date",
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True,
        required=False, )
    
    descaccident = fields.Char(
        string="Déscription",
        required=False, )
    
    img = fields.Binary(
        string="Photo",  )
