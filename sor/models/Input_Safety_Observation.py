# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError

class Observation(models.Model):
    _name = 'observation.hse'
    _inherit = ['mail.thread']
    _rec_name = 'risque_critique'
    _description = "Observation"

    reference = fields.Char(
        string='Référence SOR',
        readonly=True,
        default=lambda self: _('New'))

    projet_id = fields.Many2one(
        'project.project',
        string="Projet",
        required=False, )

    zone = fields.Many2one(
        'local.n',
        string="Zone concernée",
        required=False, )

    company_id = fields.Many2one(
        'res.company',
        string="Entreprise",
        required=False, )

    date_creation = fields.Datetime(
        string="Date creation",
        required=False,
        default=lambda s: fields.Datetime.now(),
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
        required=False, )

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High')
    ], size=1)

    _defaults = {
        'priority': '0',
    }
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('normal', 'En Progrès'),
        ('done', 'Resolu'),
        ('blocked', 'Refuser')],
        string='Kanban State',
        copy=False,
        default='draft',
        required=True)
    @api.model
    def create(self, vals):
        if vals:
            vals['reference'] = self.env['ir.sequence'].next_by_code('observation.hse') or _('New')
            res = super(Observation, self).create(vals)
            res.state = 'normal'
            return res

    def informer_responsable(self):

        message_body = "Bonjour " + self.id_soumetteur.name + "," + \
                           "<br>Vous avez recu un input Urgent  " + \
                            "<br>Type de risque : " + self.risque_critique.type_risque + \
                           "<br>Date : " + str(self.date_creation) + \
                           '<br><br>Cordialement'

        to = "adham.baq@gmail.com"
        data = {
            'subject': 'Observation Urgent',
            'body_html': message_body,
            'email_from': self.env.user.company_id.email,
            'email_to': to
            }
        template_id = self.env['mail.mail'].create(data)
        if self.env['mail.mail'].send(template_id):
                print("5/5")
        else:
                print("0/5")

    @api.multi
    def create_action(self):
        action_obj = self.env["action"]
        for rec in self:
            if rec.reference:
                action_sor = {
                    'source': 'SOR',
                    'originateur': rec.id_soumetteur.name,
                    'categorie': rec.risque_critique.type_risque,
                    'etat': 'Ouvert',
                    'responsable': self.env.user.name,
                    'date_creation': datetime.datetime.now(),
                    'type_action': 'Preventive'
                }

                action_ids = action_obj.create(action_sor)
                action_id = action_ids.id

                view_id = self.env.ref('hse_action.action_form_view').id
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

    @api.multi
    def Print_SOR(self):
        return self.env.ref('sor.print_sor_reporting').report_action(self)


class Risque(models.Model):
    _name = 'risque.r'
    _rec_name = 'type_risque'

    type_risque = fields.Char(
        string="Type Risque",
        required=True)
