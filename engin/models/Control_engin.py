# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Control_engin(models.Model):
    _name = 'control.engin'
    etat_bip_recul = fields.Selection(string='Etat bip recul',
                                      selection=[('conf', 'Conforme'), ('nconf', 'Non conforme')],
                                      )
    etat_retroviseur = fields.Selection(string='Etat rétroviseur',
                                        selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ],)
    etat_ceinture = fields.Selection(string='Etat ceinture',
                                     selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ], )
    etat_exticteur = fields.Selection(string='Etat extincteur',
                                      selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ],
                                      )
    etat_frein = fields.Selection(string='Etat frein',
                                  selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ],
                                  )
    etat_eclairage = fields.Selection(string='Etat éclairage',
                                      selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ],

                                      )
    etat_gyrophare = fields.Selection(string='Etat gyrophare',
                                      selection=[('conf', 'Conforme'), ('nconf', 'Non conforme'), ],

                                      )
    date_control = fields.Date(string='Date du contrôl', )
    engin_id = fields.Many2one('engin', string='Engin')
    # agent_contr = fields.Many2one('agent.a', string='controlé par')
    current_user = fields.Many2one('res.users', 'Controlé par', default=lambda self: self.env.user)

    # @api.model
    # def create(self, values):
    #     for v in values:
    #         if not v['etat_bip_recul']:
    #             raise
