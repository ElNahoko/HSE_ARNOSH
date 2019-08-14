from odoo import models, fields,api
from odoo.exceptions import UserError, AccessError, ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def add_to_group_special_agent(self):
        group = self.env['res.groups'].search([('name', '=', 'Agent')])  #search for my custom group
        user_id = self.id  # get the current user id
        group.users = [user_id]  # add the user to the group

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        res.add_to_group_special_agent() # add the new user to the agent group
        return res