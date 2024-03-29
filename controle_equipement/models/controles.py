# -*- coding: utf-8 -*-
import datetime
from odoo import fields, api, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


# une alert de control d'un equipement ,( envoyé par le respHSE reçus par l'employé technicien )
class alertControle(models.Model):
    _name = 'alert.alert'
    _inherit = ['mail.thread']
    _description = "demande de controle"

    name = fields.Char(
        string='Sujet controle',
    )
    equipement_id = fields.Many2one(
        'equipment.ctl', string='Equipement'
    )
    cat_equipement = fields.Char(
        related='equipement_id.cat_name',
        readonly=True
    )
    ref_equipement = fields.Char(
        related='equipement_id.ref_equip',
        readonly=True
    )
    date_planif = fields.Date(
        string="Planifié le ",
        required=True,
    )
    user_tech = fields.Char(
        related='equipement_id.tec_name',
        store=True, readonly=True
    )
    mail_tech = fields.Char(
        related='equipement_id.mail_tec',
        store=True, string="envoyé à"
    )
    local_control = fields.Char(
        related='equipement_id.local_name',
        store=True, readonly=True
    )
    description = fields.Char(
        string='description',
    )
    date_creation = fields.Datetime(
        string="date creation",
        default=lambda s: fields.Datetime.now(),
        readonly=True
    )
    date_envoi = fields.Datetime(
        string="Date d'envois",

    )
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('created', 'Non envoyé'),
        ('sent', 'Envoyé'),
    ],
        string='Status',
        copy=False,
        default='draft',
        required=True
    )

    # functions
    @api.model
    def create(self, values):
        if values:
            # vals['reference'] = self.env['ir.sequence'].next_by_code('observation.hse') or _('New')
            res = super(alertControle, self).create(values)
            res['status'] = 'created'
            # send the alert via mail
            self.send_mail_to_technicien()
            return res

    # update date_envoi when state is "sent"
    @api.onchange('status')
    def _onchange_date_envoi(self):
        if self.status == 'sent':
            self.date_envoi = fields.Datetime.now()
            # self.write({'date_envoi': fields.Datetime.now()})  # still not working ...!

    # envois par mail une demande de contrôle
    @api.one
    def send_mail_to_technicien(self):
        message_body = "Bonjour , " + self.mail_tech + \
                       "<br>Vous avez reçus une nouvelle demande de contrôle" + \
                       "<br/><ul>" + \
                       "<h2>Equipement Référencé par :" + self.ref_equipement + "</h2>" + \
                       "<li>Sujet :" + self.name + "</li>" + \
                       "<li> De catégorie :" + self.cat_equipement + "</li>" + \
                       "<li> Trouvé dans la localisation suivante :" + self.local_control + "</li>" + \
                       "<li> Date Plannifié: " + str(self.date_planif) + "</li></ul>" + \
                       "</ul><br/>" + self.description + \
                       "Veuillez remplire le formulaire de contrôle de cet équipement, " + \
                       '<br/>Cordialement,' + str(self.env.user.company_id.name) + '.'
        # to = str(self.mail_tech)   noha.drakus123@gmail.com self.env['agent.modul'].browse(id).mail_emp
        data = {
            'subject': "Contrôle d'un équipement",
            'body_html': message_body,
            'email_from': self.env.user.company_id.email,
            'email_to': self.mail_tech
        }
        template_id = self.env['mail.mail'].create(data)
        self.env['mail.mail'].send(template_id)  # browse
        if template_id:
            self.date_envoi = fields.Datetime.now()
            return self.write({'status': 'sent'})
            print("sent !")
        else:
            print("not sent :(")
            # raise ValidationError("Oups , échec d envois ! veulliez réssayer plutard ")
