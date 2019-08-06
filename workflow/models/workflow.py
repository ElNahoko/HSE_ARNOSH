from odoo import api, fields, models,exceptions


class Agent(models.Model):
    _name = 'agent.a'

    agent_id = fields.Many2one(
        'res.users',
        string='Agent',
        default=lambda s: s.env.user)
    agent_image = fields.Binary(string='Photo')
    local_id = fields.One2many('local.n', 'Localisation_Af', string='Localisation')

class Localisation(models.Model):
    _name = 'local.n'
    _rec_name = 'localisation'
    _description = 'New Description'

    Localisation_Af = fields.Many2one('agent.a', string='Localisation', readonly=True)
    localisation = fields.Char(string="Nom du Zone ", required=True, )
    date_creation = fields.Datetime(string='Date Creation', default=lambda s: fields.Datetime.now(), invisible=False, readonly=True)






























