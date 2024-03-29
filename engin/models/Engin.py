# -*- coding: utf-8 -*-
from os.path import join

from odoo import models, fields, api

class TypeEngin(models.Model):
    _name = 'type.engin'
    _rec_name = 'nom'

    nom = fields.Char(string="Type d'engin ou vehicule", required=True)


class Engin(models.Model):
    _inherit = ['mail.thread']
    _name = 'engin'
    _rec_name = 'matricule'
    _sql_constraints = [('matricule_unique', 'unique(matricule)', 'déjà trouvé')]

    type = fields.Many2one('type.engin', string="Type d'engin ou vehicule", required=True)
    matricule = fields.Char(string='Matricule', required=True)
    date_fin_assurance = fields.Date(string='Date fin Assurance', required=True)
    control_id = fields.One2many('control.engin', 'engin_id', string='Contrôles')
    agent_id = fields.Many2one('agent.a', string='Conducteur')
    image_carte = fields.Binary(string="Documents (carte grise..)")
    engin_idC = fields.Many2one('pro.control', string='Engins')

    @api.multi
    def Controler_engin(self):
        self.ensure_one()

        control = self.env['control.engin'].create({'engin_id': self.id})
        control_id = control.id

        return {
            'name': ('Controler engin ', self.matricule),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'control.engin',
            'view_id': self.env.ref('engin.engin_cview').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': control_id
        }


class demandeControl(models.Model):
    _inherit = ['mail.thread']
    _name = 'pro.control'
    _rec_name = 'sujet'

    sujet = fields.Char(string='Sujet de la demande', required=True)
    enginP_id = fields.Many2many('engin', string='Engin', required=True)
    matricule_en = fields.Char(related='enginP_id.matricule')
    date_du_control = fields.Date(string='Date du contrôl', required=True)
    agent_control = fields.Many2one('res.users', String="envoyé à", )
    mail_ag = fields.Char(related='agent_control.email')
    commentaire = fields.Char(String="Commentaire", required=True)
    state = fields.Selection([
        ('outgoing', "En cours d'envoi"),
        ('sent', 'Envoyé'),
    ], 'Status', readonly=True, copy=False, default='outgoing')

    # @api.multi
    # def demanderc(self):
    #     self.ensure_one()
    #
    #     control = self.env['mail.mail'].create({'engin_id': self.id})
    #     control_id = control.id
    #
    #     data = {
    #         'subject': 'Control d engin ',
    #         'email_from': self.env.user.company_id.email,
    #
    #     }
    #
    #     template_id = self.env['mail.mail'].create(data).id
    #
    #     return {
    #         'name': ('Demande de control'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'mail.mail',
    #         'view_id': self.env.ref('mail.view_mail_form').id,
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #         'res_id': template_id
    #     }

    @api.multi
    def demanderc(self):
        print(*str(self.enginP_id), sep=", ")

        message_body = "Bonjour " + self.agent_control.name + "," + \
                       "<br>Vous avez une demande de contrôl  " + \
                       "<br>Engin(s) : " + ''.join(str(e.matricule) + ' ,' for e in self.enginP_id) + \
                       "<br>Date du contrôl : " + str(self.date_du_control) + \
                       "<br> Commentaire : " + str(self.commentaire) + \
                       '<br><br>Cordialement'
        to = self.mail_ag

        data = {
            'subject': self.sujet,
            'body_html': message_body,
            'email_from': self.env.user.company_id.email,
            'email_to': to
        }

        template_id = self.env['mail.mail'].create(data)
        # self.env['mail.mail'].browse(template_id.id).send(self.id)
        # sending = self.env['mail.mail'].send(template_id)
        self.env['mail.mail'].browse(template_id.id).send(self.id)
        self.write({'state': 'sent'})
