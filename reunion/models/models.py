# -*- coding: utf-8 -*-

from odoo import models, fields


class reunion(models.Model):
    _name = 'reunion'
    _rec_name = 'titre'

    type = fields.Selection([('formation', 'Formation'), ('tolbox', 'Toolbox')], string='Type réunion', required=True)

    titre = fields.Char(string='Nom reuinion', )
    duree = fields.Selection(
        [('2', '2 min'), ('5', '5 min'), ('10', '10 min'), ('20', '20 min'), ('30', '30 min'), ('45', '45 min'),
         ('60', '1 H')], string='Durée de la réuinion', required=True)
    responsable = fields.Many2one('agent.a', string='Responsable de la réuinion')

    nbr = fields.Integer(string='Nombre de participants', )
    date = fields.Date(string='Date de réuinion')
    etat = fields.Selection([('cloturé', 'cloturé'), ('programmé', 'programmé')], string='Etat de la réunion')
    photo = fields.Binary(string='Fiche de présence')
    rapport = fields.Char(string='rapport de la réunion')
    #particip = fields.One2many('agent.a', 'id', string='Les participants')
