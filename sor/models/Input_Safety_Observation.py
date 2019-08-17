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
    kanban_state = fields.Selection([
        ('normal', 'En Progres'),
        ('done', 'Resoly'),
        ('blocked', 'Refuser')], string='Kanban State',
        copy=False, default='normal', required=True)

    observation_refuser = fields.Char(
        'Red Kanban Label',
        default=lambda s: _('Refuser'),
        required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the observation or issue is in that stage.')
    observation_resolu = fields.Char(
        'Green Kanban Label',
        default=lambda s: _('Resolu'),
        required=True,
        help='Override the default value displayed for the done state for kanban selection, when the observation or issue is in that stage.')
    observation_normal = fields.Char(
        'Grey Kanban Label',
        default=lambda s: _('In Progress'),
        required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the observation or issue is in that stage.')
    auto_validation_kanban_state = fields.Boolean(
        'Automatic kanban status',
        default=False,
        help="Automatically modify the kanban state when the HSE REPONSIBLE CREATE THE OBSERVATION ACTION for this SOR.\n"
            " * THE FOLLOWING ACTION from the RESPONSIBLE will update the kanban state to 'RESOLU' (green bullet).\n")

    @api.model
    def create(self, vals):
        if vals:
            vals['reference'] = self.env['ir.sequence'].next_by_code('observation.hse') or _('New')
            return super(Observation, self).create(vals)

    def informer_responsable(self):
            message_body = "Bonjour " + self.id_soumetteur.name + "," + "<br>Vous avez recu un input Urgent  " \
                                             + "<br>Type de risque : " + self.risque_critique.type_risque + "<br>Date : " + str(self.date_creation) + \
                       '<br><br>Cordialement'
            to = "hamza.natsu@gmail.com"
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
                    'originateur': rec.id_soumetteur,
                    'categorie': rec.risque_critique.type_risque,
                    'etat': 'Ouvert',
                    'date_creation': str(datetime.datetime.now()),
                }
                action_ids = action_obj.create(action_sor)
                action_id = action_ids.id

                view_id = self.env.ref('action.ACTION_FORM_VIEW').id

                return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'action',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('SOR Action'),
                    'res_id': action_id
                }

class Risque(models.Model):
    _name = 'risque.r'
    _rec_name = 'type_risque'

    type_risque = fields.Char(
        string="Type Risque",
        required=True)
