from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError

class Agent(models.Model):
    _name = 'agent.a'
    _rec_name = 'agent_id'


    agent_id = fields.Many2one(
        'res.users',
        string='Agent',
        default=lambda s: s.env.user, index=True)
    
    agent_image = fields.Binary(
        string='Photo
        
    type_compte = fields.Selection(
        string="Type de Compte",
        selection=[('special', 'Agent Special'),
                  ('normaux', 'Agent normale'), ],
        required=True, )
        
    local_id = fields.One2many(
        'local.n',
        'Localisation_Af',
        string='Localisation')
        
    titre = fields.Selection([
         ('mr', 'Mr'),
         ('mme', 'Mme'),
         ('mlle', 'Mlle'),
    ], string='Titre', default='mr', required=True)

    @api.model
    def create(self, vals):
        if vals.get('agent_id',False):
            modelObj = self.env['agent.a']
            rec = modelObj.search([('agent_id', '=', vals.get('agent_id',False))])
            if rec:
                raise ValidationError(('Already exists'))
        return super(Agent, self).create(vals)


class Localisation(models.Model):
    _name = 'local.n'
    _rec_name = 'localisation'
    _description = 'New Description'

    Localisation_Af = fields.Many2one(
        'agent.a',
        string='Localisation',
        readonly=True)
        
    localisation = fields.Char(
        string="Nom du Zone ",
        required=True, )
        
    date_creation = fields.Datetime(
        string='Date Creation',
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True)






























