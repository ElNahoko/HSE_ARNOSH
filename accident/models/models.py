# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api , _

class regle(models.Model):
    _name = 'reg.reg'
    _rec_name = 'nom'

    nom = fields.Char(string="Règle", required=False, )
    icon = fields.Binary(string="Icone",  )
    desc = fields.Char(string="Description", required=False, )

class gravite(models.Model):
    _name = 'gra.gra'
    _rec_name = 'grav'

    grav = fields.Char(string="Gravité", required=False, )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      


class accident(models.Model):
    _name = 'acc.acc'
    _rec_name = 'type'

    id_soumetteur = fields.Many2one(
        'res.users',
        string='Agent',
        default=lambda s: s.env.user,
        readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('normal', 'En Progrès'),
        ('done', 'Resolu'),
        ('blocked', 'Refuser')],
        string='Kanban State',
        copy=False,
        default='draft',
        required=True)
    type = fields.Selection(string="Type", selection=[('Accident', 'Accident'), ('Incident', 'Incident'), ], required=False, )
    gravite = fields.Many2one('gra.gra', string="Gravité", required=False, )
    regle = fields.Many2one('reg.reg', string="Règle de sécurité", required=False, )
    date = fields.Datetime(string="Date",default=lambda s: fields.Datetime.now(),invisible=False,readonly=True, required=False, )
    descaccident = fields.Char(string="Déscription", required=False, )
    img = fields.Binary(string="Photo",  )


    @api.model
    def create(self, vals):
        if vals:
            vals['reference'] = self.env['ir.sequence'].next_by_code('observation.hse') or _('New')
            res = super(accident, self).create(vals)
            res.state = 'normal'
            return res


    @api.multi
    def print_accident(self):
        return self.env.ref('accident.action_report_accident').report_action(self)

    @api.multi
    def create_action(self):
        action_obj = self.env["action"]
        for rec in self:
           action_sor_accident = {
                'source': 'Accident',
                'originateur': rec.id_soumetteur.name,
                'gravite': rec.gravite.grav,
                'etat': 'Ouvert',
                'date_creation': datetime.datetime.now()
                }
           action_sor_incident = {
                'source': 'Incident',
                'originateur': rec.id_soumetteur.name,
                'gravite': rec.gravite.grav,
                'etat': 'Ouvert',
                'date_creation': datetime.datetime.now()
            }

           if rec.type == 'Incident':
                action_idinc = action_obj.create(action_sor_incident)
                action_id = action_idinc.id

           if rec.type == 'Accident':
                action_idacc = action_obj.create(action_sor_accident)
                action_id = action_idacc.id

           view_id = self.env.ref('action.action_form_view').id
           self.write({'state': 'done'})
           return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'action',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('SOR Action'),
                    'res_id': action_id
                }

    @api.multi
    def refuser_observation(self):
        return self.write({'state': 'blocked'})
