import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError


class Agent(models.Model):
    _name = 'agent.a'
    _rec_name = 'agent_id'
    _inherit = ['mail.thread']

    agent_id = fields.Many2one(
        'res.users',
        string='Agent',
        default=lambda s: s.env.user, index=True)

    agent_image = fields.Binary(
        string='Photo')

    type_compte = fields.Selection(
        string="Type de Compte",
        selection=[('special', 'Agent Special'),
                   ('normaux', 'Agent normale'), ],
        required=True, track_visibility='onchange')

    local_id = fields.One2many(
        'local.n',
        'Localisation_Af',
        string='Localisation', track_visibility='onchange')

    titre = fields.Selection([
        ('mr', 'Mr'),
        ('mme', 'Mme'),
        ('mlle', 'Mlle'),
    ], string='Titre', default='mr', required=True)

    cin = fields.Char(
        string="CIN",
        required=True, )

    sous_traitant = fields.Many2one(
        'res.users',
        string='Sous Traitant', )

    poste = new_field = fields.Char(
        string="Poste Occupee",
        required=False, )

    date_induction = fields.Datetime(
        string='Date Induction', )

    @api.model
    def create(self, vals):
        if vals.get('agent_id', False):
            modelObj = self.env['agent.a']
            rec = modelObj.search([('agent_id', '=', vals.get('agent_id', False))])
            if rec:
                raise ValidationError(('Compte utilisateur existe déjà'))
            else:
                self.create_action()
            return super(Agent, self).create(vals)

    @api.multi
    def create_action(self):
        for agent in self:
            for line in agent.local_id:
                action_obj = self.env["historiq"]
                values = [(0, 0, {'localisation': value.localisation}) for value in line]
                historique = {
                'date_affectation': str(datetime.datetime.now()),
                'nom_agent': agent.agent_id.name,
                'post_occupee': agent.poste,
                'zone_affecte': values,}
                action_ids = action_obj.create(historique)



class Localisation(models.Model):
    _name = 'local.n'
    _rec_name = 'localisation'
    _description = 'New Description'

    Localisation_Af = fields.Many2one(
        'agent.a',
        string='Localisation',
        readonly=True)
    Localisation_Af_hist = fields.Many2one(
        'historiq',
        string='Local Historique',
        readonly=True)

    localisation = fields.Char(
        string="Nom du Zone ",
        required=True, )

    parent_id = fields.Many2one(
        'local.n',
        string='Parent Category',
        ondelete='restrict',
        index=True)

    image = fields.Binary(
        string="Image du zone",  )

    risque_du_zone = fields.Text(
        string="Les Risques du Zone",  )

    child_ids = fields.One2many(
        'local.n', 'parent_id',
        string='Child Categories')

    date_creation = fields.Datetime(
        string='Date Creation',
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive Zone.')


    class Historique(models.Model):
        _name = 'historiq'
        _rec_name = 'nom_agent'
        _description = 'Historique des affectations'

        date_affectation = fields.Char(
            string="",
            required=False, )

        nom_agent = fields.Char(
            string='Agent',
            index=True)

        post_occupee = fields.Char(
            string="Post Occupée",
            required=False, )

        zone_affecte = fields.One2many(
            'local.n',
            'Localisation_Af_hist',
            string='Zone Affecté', track_visibility='onchange')


























