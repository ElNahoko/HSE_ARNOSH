import datetime
from passlib.handlers import django
from odoo import api, fields, models, SUPERUSER_ID, _

# localisation inherited from workflow module
from odoo.fields import Char


class Controles(models.Model):
    _name = 'controle.ctl'
    _inherit = ['mail.thread']
    _rec_name = 'ref_ctl'

    ref_ctl = fields.Char(
        string='Réference',
        readonly=True,
        index=True, default=lambda self: _('New')
    )
    # ----equipement infos ---
    equip_id = fields.Many2one(
        'equipment.ctl', string='Equipement'
    )
    equip_categorie = fields.Char(
        string="Catégorie",
        related='equip_id.cat_name',
        readonly=True
    )
    type_equip = fields.Char(
        string='Type',
        related='equip_id.nom_equip',
        readonly=True
    )
    date_control = fields.Datetime(
        string="Date du contrôle ",
        default=lambda s: fields.Datetime.now(),
    )
    controle_type = fields.Selection(
        [('1', 'Journalier'), ('2', 'Hebdomadaire'),
         ('3', 'Mensuel'), ('4', 'Annuelle')],
        string=' Contrôle', default="3"
    )
    user_tech = fields.Char(
        string='Contrôleur',
        default=lambda self: self.env.user.name,
        readonly=True
    )
    date_creation = fields.Datetime(
        string="date creation",
        default=lambda s: fields.Datetime.now(),
        readonly=True
    )
    comment = fields.Char(
        string='commentaire',
    )
    conforme = fields.Selection([
        ('o', 'Oui'),
        ('n', 'Non'),
    ], string='Comforme',
        default='n',
    )
    # boolean fields for conform.field -->in order to make a checkbox in view
    # _columns = {
    #     'o': fields.Boolean('Oui'),
    #     'n': fields.Boolean('Non'),
    # }
    state = fields.Selection([
        ('done', 'Résolut'),
        ('notyet', 'En cours'),  # en cours
    ],
        default='notyet',
    )

    # creation d'une sequence unique pour contrôle
    @api.model
    def create(self, vals):
        if vals:
            vals['ref_ctl'] = self.env['ir.sequence'].next_by_code('control_seq') or _('New')
        return super(Controles, self).create(vals)

    # @api.multi
    # def print_controle(self):
    #     return self.env.ref('controle.ctl.controles_report').report_action(self)


class Equipement(models.Model):
    _name = 'equipment.ctl'
    _rec_name = 'ref_equip'

    ### infos equipement : ###
    ref_equip = fields.Char(
        string='Réference',
        readonly=True,
        default=lambda self: _('New')
    )
    nom_equip = fields.Char(
        string="Type",
        required=True
    )  # search='_search_equipement' ,
    categorie_id = fields.Many2one(
        'categorie.ctl',
        string='Catégorie',
        required=True
    )
    localisation_id = fields.Many2one(
        'local.n', string='Localisation',
        required=True
    )
    local_parent =fields.Char(
        string ='local supérieur',
        related='localisation_id.parent_name'
    )
    utilisation = fields.Char(
        string="Utilisation",
    )
    quantity = fields.Float(
        string="Quantité",
        default="1",
    )
    #unité de mesure pr qté
    unite_mesure = fields.Selection(
        [('1', 'unité'), ('2', 'Kl'),
         ('3', 'L'), ('4', 'g')],
        string='msuré par ', default="1"
    )
    commentaire = fields.Text(
        string="Description",
    )
    technician_user_id = fields.Many2one(
        'res.users', 'Responsable Technique', required=True
    )
    # related fields -->to be used in controle models..----
    cat_name = fields.Char(
        related='categorie_id.name',
        store=True
    )
    mail_tec = fields.Char(
        related='technician_user_id.email',
        store=True
    )
    tec_name = fields.Char(
        related='technician_user_id.name',
        store=True
    )
    local_name = fields.Char(
        related='localisation_id.localisation',
        store=True
    )  # ------------------------------------------------------
    controle_ids = fields.One2many(
        'controle.ctl', 'equip_id'
    )
    ## infos de type de controles pour cet équipement ##
    controle_count = fields.Integer(
        string="Nombre de controles",
        compute='_compute_controle_count',
    )
    type_controle = fields.Selection(
        [('1', 'Journalier'), ('2', 'Hebdomadaire'),
         ('3', 'Mensuel'
          ), ('4', 'Annuelle')],
        string=' Type de maintenance', default="3"
    )
    periode = fields.Char(
        string='Nombre de jours entre contrôles.',
        default="30",
        # compute='_depends_periode_type'
    )
    date_utilisation = fields.Date(
        string='Date de mise en charge',
        default=fields.Date.context_today
    )
    date_creation = fields.Datetime(
        string='Date Creation',
        default=lambda s: fields.Datetime.now(),
        invisible=False,
        readonly=True)

    @api.model
    def create(self, vals):
        if vals:  # creation d'une sequence unique pour équipement
            vals['ref_equip'] = self.env['ir.sequence'].next_by_code('equip_seq') or _('New')
        return super(Equipement, self).create(vals)

    #   count number of controle done for this equip"
    @api.multi
    def _compute_controle_count(self):
        for control in self:
            control.controle_count = len(control.controle_ids)

    # @api.onchange('type_controle')
    # def _onchange_periode_type(self):
    #     for rec in self:
    #         selected = rec._fields['type_controle'].get_values(self.env)
    #         print(selected)
    #         if selected == "Journalier":  # if rec.type_controle == '1':
    #            rec.periode = '1'  # Journalier
    #         elif selected == "Hebdomadaire":
    #            rec.periode = '7'  # Hebdomadaire
    #         elif selected == "Mensuel":
    #            rec.periode = '30'  # Mensuel
    #         else:
    #            rec.periode = '365'  # Annuelle

    #   Responsable Tech vas créer un contrôle qui a fait pour cet equipement. et remplire formulair
    # création d'un controle pour un equipement
    @api.multi
    def ajout_controle(self):
        ctl_obj = self.env["controle.ctl"]
        # for rec in self:
        #     if rec.ref_equip:
        #         # control = {
        #         #     'controle_type': rec.type_controle,
        #         #     'equip_id': rec.id,
        #         #     #  'date_demande': datetime.datetime.now()
        #         # }
        control_create = ctl_obj.create({'equip_id': self.id})
        control_id = control_create.id

        view_id = self.env.ref('controle_equipement.ctl_view_form').id
        # retourné la vue du controle
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'controle.ctl',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'name': _('Controles'),
            'res_id': control_id
        }


class Categorie(models.Model):
    _name = 'categorie.ctl'

    name = fields.Char('Nom catégorie', required=True, translate=True)
    image_categorie = fields.Binary(
        string='Image catégorie',
        required=True)
    note = fields.Text(
        'Description', translate=True
    )
    equip_ids = fields.One2many(
        'equipment.ctl', 'categorie_id',
        string='Equipments', copy=False,

    )


# localisation herited from workflow.localisation
class Localisation_ctl(models.Model):
    _inherit = 'local.n'

    equipements_id = fields.One2many(
        'equipment.ctl', 'localisation_id',
        string='Equipments', readonly=True,
        invisible=True
    )

    # the employees related to this location
    # agents_related = fields.One2many(
    #    'agent.a', 'agent_id', string='Agents disponibles',
    #    help='Agents qui travaillent dans cette localisation',
    #    readonly=True)
