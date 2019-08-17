import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class Action(models.Model):
    _name = "action"

    # N° de référence de l'action pour permettre un suivis
    reference_action = fields.char(
        string="Reference Action",
        readonly=True,
        default=lambda self: _('New'))

    # Indiquer d’où vient l'action.
    source = fields.Char(
        string="Type Risque",
        required=False, )

    # Description de l'observation
    description_observation = fields.Text(
        string="",
        required=False, )

    # La personne qui a fait l'observation
    originateur = fields.Char(
        string="",
        required=False, )

    #  Catégories SOR
    categorie = fields.Char(
        string="",
        required=False, )

    #Action prise ou à prendre pour corriger l'anomalie
    action_correctif = fields.Text(
        string="",
        required=False, )

    # Date à laquelle l'action corrective doit être cloturée
    delai = fields.Date(
        string="delai",
        required=False, )

    # Closed = Cloturée; Open = Ouvert
    etat = fields.Selection(
        string="",
        selection=[('Cloturee', 'Closed'),
                   ('Ouvert', 'Open'), ],
        required=False, )

    # Responsable du suivis de l'action
    responsable = fields.Char(
        string="",
        required=False, )

    # L'entreprise chez laquelle l'observation a été faite

    entreprise = fields.Char(
        string="",
        required=False, )

    # Si l'observation est un non respect des consignes de sécurité mettre "Finding".
    # Si l'observation est positive mettre "Positive Observation"

    type = fields.Selection(
        string="",
        selection=[('finding', 'Finding'),
                   ('positive', 'Positive Observation'), ],
        required=False, )

    # Date réelle à laquelle l'action a été cloturée
    date_cloture = fields.Datetime(
        string="",
        required=False, )
    # Date du creation de l'action
    date_creation = fields.Datetime(
        string="",
        required=False, )

    @api.model
    def create(self, vals):
        if vals:
            vals['reference_action'] = self.env['ir.sequence'].next_by_code('action') or _('New')
            return super(Action, self).create(vals)
