import datetime

from passlib.handlers import django

from odoo import api, fields, models, SUPERUSER_ID, _

# localisation inherited from workflow module
from odoo.fields import Char


class Localisation_inherit(models.Model):
   # _name = 'local.n'
   # _inherit = ['local.n', 'agent.a']
    _inherit = 'local.n'

    equipements_id = fields.One2many('g.equipment', 'localisation_id', string='Equipments',readonly=True, invisible =True)
    # the employees related to this location
    #agents_related = fields.One2many(
    #    'agent.a', 'agent_id', string='Agents disponibles',
    #    help='Agents qui travaillent dans cette localisation',
    #    readonly=True)


class Equipement(models.Model):
    _name = 'g.equipment'
    _rec_name = 'Nom_equip'

    ### infos equipement : ###
    reference = fields.Char(string='Réference', required=True, readonly=True,
                            index=True, default=lambda self: _('New'))  # search='_search_equipement' ,  )
    Nom_equip = fields.Char(string="Nom d'équipement", required=True)  # search='_search_equipement' ,
    categorie_id = fields.Many2one('categorie.equipement', string='Catégorie')
    localisation_id = fields.Many2one('local.n', string='Localisation')

    utilisation = fields.Char(string="Utilisation", required=True)
    quantity = fields.Float(string="Quantité", default="1", )
    emplacement = fields.Char(string="Emplacement", required=True)
    commentaire = fields.Text(string="Description", )

    technician_user_id = fields.Many2one('res.users', 'Responsable Technique',  # track_visibility='onchange',
                                         default=lambda self: self.env.uid, oldname='user_id')
    maintenance_ids = fields.One2many('demande.maint', 'equipement_id')

    ## infos maintenance pour cet equipement: ##
    #periode = fields.Integer('Nombre de jours entre maintenances.')
    type_maintenance = fields.Selection(
        [('1', 'Journalier'), ('2', 'Hebdomadaire'), ('3', 'Mensuel'), ('4', 'Anuelle')],
        string=' Type de Maintenance', default="Mensuel")
    #maintenance_duration = fields.Float(help="Durée de Maintenance par heur.")

    ## date de première utilisation de l"equipement , today by default ##
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


    @api.multi
    def create_demande_maint(self):

        dem_maint_obj = self.env["demande.maint"]
        for rec in self:
            if rec.reference:
                demande_maint = {
                    'maintenance_type' : rec.type_maintenance,
                    'equipement_id': rec.id,
                    'user_id': rec.technician_user_id.id,
                    'date_demande': datetime.datetime.now()
                }

                demande_create = dem_maint_obj.create(demande_maint)
                demande_id = demande_create.id

                view_id = self.env.ref('g__materiel.demande_maint_form_view').id

                return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'demande.maint',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('Maintenance'),
                    'res_id': demande_id
                }
# calculer la date de prochaine maintenance

class Categorie(models.Model):
    _name = 'categorie.equipement'

    name = fields.Char('Nom catégorie', required=True, translate=True)

    note = fields.Text('Description', translate=True)
    equipment_ids = fields.One2many('g.equipment', 'categorie_id', string='Equipments', copy=False, readonly=True, invisible =True)


#  demande de maintenance :
class DemandeDeMaintenance(models.Model):
    _name = 'demande.maint'
    #_inherit = ['mail.thread']

    name = fields.Char('Sujet', require=True)
    maintenance_type = fields.Selection([('1', 'Journalier'),('2', 'Hebdomadaire'),('3', 'Mensuel'), ('4', 'Anuelle')],
                                        string='Maintenance Type', default="Mensuel")
    description = fields.Text(string="Description", )
    date_demande = fields.Date('Demandé le', default=fields.Date.context_today,
                               help="Date de lancement de la demande de maintenance ")
    date_planif = fields.Date('Plannifié le', default=fields.Date.context_today,
                              help="Date de la plannification de maintenance ")
    user_id = fields.Many2one('res.users', string='Responsable Technique',  # track_visibility='onchange',
                              oldname='technician_user_id',  help="l'employé qui seras responsable pour cette maintenance")
    equipement_id = fields.Many2one('g.equipment', string='Equipement')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent'), ('2', 'Très Urgent')], string='Priorité')
    duree = fields.Float(help="Durée de Maintenance par heur.")


