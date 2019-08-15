# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests


class ResUserLog(models.Model):
    _inherit = 'res.users.log'
    # Localisation d'authentification de l'Agent
    Localisation = fields.Char()

    # date authenticiation de l'Agent
    date_authentification = fields.Datetime(
        compute="_get_authentification_date",
        string="Date d'authentification")

    @api.multi
    def _get_authentification_date(self):
        for record in self:
            record.date_authentification = record.create_date


class ResUser(models.Model):

    _inherit = 'res.users'

    @api.model
    def _update_dernier_authentification(self):
        vals = {}
        # recuperer les info dans un fichier .json
        url = 'http://ipinfo.io/json'
        request = requests.get(url)
        js = request.json()
        ville = js['city']
        region = js['region']
        pays_code = js['country']
        country_id = self.env['res.country'].search([('code', '=', pays_code)], limit=1)
        for pays in country_id:
            address = ville + ', ' + region + ', ' + pays.name
        vals.update({
            'location': address,
            'user_id': self.env.user.id})
        # Créer un objet user_log
        agent_log_id = self.env['res.users.log'].create(vals)
        agent = self.env.user
        agent.write({'log_ids': [(6, 0, [agent_log_id.id])]})
