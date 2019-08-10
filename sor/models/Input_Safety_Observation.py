# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Observation(models.Model):
    _name = 'observation.hse'
    _rec_name = 'risque_critique'

    reference = fields.Char(
        string='Référence SOR',
        readonly=True,
        default=lambda self: _('New'))
    
    projet_id = fields.Many2one(
        'project.project',
        string="Projet",
        required=False, )
    
    company_id = fields.Many2one(
        'res.company',
        string="Entreprise",
        required=False, )
    
    date_creation = fields.Datetime(
        string="Date creation",
        required=False,default=lambda s: fields.Datetime.now(),
        readonly=True)
    
    id_soumetteur = fields.Many2one(
        'res.users',
        string='Agent',
        default=lambda s: s.env.user,
        readonly=True)
    
    image_observation = fields.Binary(
        string='Image d\'observation',
        required=True)
    
    localisation = fields.Text(
        string="Localisation",
        required=False, )
    
    description = fields.Text(
        string="Description",
        required=False, )
    
    risque_critique = fields.Many2one(
        "risque.r",
        string="Type de Risque",
        required=True, )
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High')
    ], size=1)
    
    _defaults = {
        'priority': '0',
    }

    @api.model
    def create(self, vals):
        if vals:
            vals['reference'] = self.env['ir.sequence'].next_by_code('observation.hse') or _('New')
            return super(Observation, self).create(vals)

class Risque(models.Model):
    _name = 'risque.r'
    _rec_name = 'type_risque'

    type_risque = fields.Char(
        string="Type Risque",
        required=True)
