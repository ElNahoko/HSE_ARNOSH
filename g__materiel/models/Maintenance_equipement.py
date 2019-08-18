from passlib.handlers import django

from odoo import api, fields, models, SUPERUSER_ID, _


# localisation inherited from workflow module
class Localisation_inherit(models.Model):
    _inherit = 'local.n'

    equipements_id = fields.One2many('g.equipment', 'localisation_id', string='Equipments')


class Equipement(models.Model):
    _name = 'g.equipment'
    _rec_name = 'Nom_equip'
    # local_id =fields.Many2one('local.zone',Zone affecté)

    reference = fields.Char(string='Réference', required=True, readonly=True,
                            index=True, default=lambda self: _('New'))  # search='_search_equipement' ,  )
    Nom_equip = fields.Char(string="Nom d'équipement", required=True)  # search='_search_equipement' ,
    categorie_id = fields.Many2one('categorie.equipement', string='Catégorie')
    # localisation_id = fields.Char(string="Localisation ", required=True, )
    localisation_id = fields.Many2one('local.n', string='Localisation')
    utilisation = fields.Char(string="Utilisation", required=True)
    quantity = fields.Float(string="Quantité", default="1", )
    emplacement = fields.Char(string="Emplacement", required=True)
    commentaire = fields.Char(string="Commentaire", size=100, required=True)
    # date de première utilisation de l"equipement , today by default
    date_utilisation = fields.Date(string='Date première utilisation', default=fields.Date.context_today)

    date_creation = fields.Datetime(
        string='Date Creation',
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True)


@api.model
def create(self, vals):
    if vals:
        vals['reference'] = self.env['ir.sequence'].next_by_code('equip_seq') or _('New')
    return super(Equipement, self).create(vals)


class Categorie(models.Model):
    _name = 'categorie.equipement'

    name = fields.Char('Category Name', required=True, translate=True)
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    # technician_user_id = fields.Many2one('res.users', 'Responsable', track_visibility='onchange',
    # default=lambda self: self.env.uid, oldname='user_id')
    color = fields.Integer('Couleur Index')
    note = fields.Text('Commentaire', translate=True)
    equipment_ids = fields.One2many('g.equipment', 'categorie_id', string='Equipments', copy=False, readonly=True)
