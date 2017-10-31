# -*- coding: utf-8 -*-
##############################################################################
#
#    JMR Infotech, Bank Along
#    Copyright © 2016. JMR Infotech All Rights Reserved.
#
#    With delivery and development centers in India,
#    sizable global presence and customers spread across 5 continents,
#    JMR Infotech is a leader in Information Technology solutions and services.
#    In our short existence, since 2007, we have grown to have top brands as our clients.
#
##############################################################################

from openerp import models, fields, api


class res_groups(models.Model):
    _inherit = "res.groups"

    user_type = fields.Boolean('Is User Type')


class create_user_wizard(models.TransientModel):
    _name = 'create.user.wizard'
    _description = 'Create User'
    _order = "id desc"

    primary_client = fields.Many2one('res.company', 'Primary Client')
    user_type = fields.Many2one('res.groups', 'User Type')
    f_name = fields.Char('First Name')
    l_name = fields.Char('Last Name')
    email = fields.Char('Email Address')
    login = fields.Char('Login')
    open_user = fields.Boolean('Open User Settings')
    password = fields.Char('Password')

    @api.one
    def create_user(self):
        context = self._context
        name = str(self.f_name).encode('utf-8') + ' ' + str(self.l_name).encode('utf-8')
        vals = {'name': name,
                'login': self.login,
                'password': self.password,
                'email': self.email,
                'first_name': self.f_name,
                'last_name': self.l_name,
                'company_id': self.primary_client.id
                }
        user_id = self.env['res.users'].create(vals)
        group_users = [user_id.id for user_id in self.user_type.users]
        group_users.append(user_id.id)
        self.user_type.users = [(6, 0, group_users)]
        if self.open_user:
            tree_id = self.env.ref("base.view_users_tree").id
            form_id = self.env.ref("base.view_users_form").id
            print '\n tree ', tree_id, form_id
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'res.users',
                'res_id': user_id.id,
                'target': 'current',
            }







