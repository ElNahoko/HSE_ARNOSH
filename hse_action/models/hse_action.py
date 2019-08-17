import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class Action(models.Model):
    _name = "action"
    _rec_name = "reference_action"

    # N° de référence de l'action pour permettre un suivis
    reference_action = fields.Char(
        string="Reference Action",
        readonly=True,
        default=lambda self: _('New'))

    # Indiquer d’où vient l'action.
    source = fields.Char(
        string="Type Risque",
        required=False, readonly=True,)

    # Description de l'observation
    description_observation = fields.Text(
        string="Description",
        required=False, )

    # La personne qui a fait l'observation
    originateur = fields.Char(
        string='Agent',
        readonly=True, )

    #  Catégories SOR
    categorie = fields.Char(
        string="Categorie",
        required=False,
        readonly=True,)

    #Action prise ou à prendre pour corriger l'anomalie
    action_correctif = fields.Text(
        string="Action Correctif",
        required=False, )

    # Date à laquelle l'action corrective doit être cloturée
    delai = fields.Date(
        string="delai",
        required=False, )

    # Closed = Cloturée; Open = Ouvert
    etat = fields.Selection(
        string="Etat",
        selection=[('Cloturee', 'Closed'),
                   ('Ouvert', 'Open'), ],
        required=False,
        readonly=True, )

    # Responsable du suivis de l'action
    responsable = fields.Char(
        string='Responsable',
        readonly=True)

    # L'entreprise chez laquelle l'observation a été faite

    entreprise = fields.Char(
        string = "Entreprise",
        required=False,
        readonly=True)

    # Si l'observation est un non respect des consignes de sécurité mettre "Finding".
    # Si l'observation est positive mettre "Positive Observation"

    type = fields.Selection(
        string="Type Observation",
        selection=[('finding', 'Finding'),
                   ('positive', 'Positive Observation'), ],
        required=False, )

    # Date réelle à laquelle l'action a été cloturée
    date_cloture = fields.Datetime(
        string="Date cloture",
        required=False, )

    # Date du creation de l'action
    date_creation = fields.Datetime(
        string="Date creation",
        required=False,
        default=lambda s: fields.Datetime.now(),
        readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('source') == 'SOR':
            vals['reference_action'] = self.env['ir.sequence'].next_by_code('action.sor') or _('New')
            return super(Action, self).create(vals)
        elif vals.get('source') == 'Accident':
            vals['reference_assction'] = self.env['ir.sequence'].next_by_code('action.acci') or _('New')
            return super(Action, self).create(vals)
        elif vals.get('source') == 'Incident':
            vals['reference_action'] = self.env['ir.sequence'].next_by_code('action.inci') or _('New')
            return super(Action, self).create(vals)
