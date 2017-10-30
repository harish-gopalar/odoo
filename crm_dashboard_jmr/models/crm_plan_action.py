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

from openerp import models, fields, api, exceptions, _
from datetime import datetime
from openerp.osv.orm import setup_modifiers
from lxml import etree
import re


class plan_opportunities_line(models.Model):
    _name = 'plan.opportunities.line'
    _description = 'Plan Opportunities Line'
    _order = "id desc"
    _rec_name = 'opportunity_id'

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity Name', required=True)
    partner_id = fields.Many2one('res.partner', 'Account Name', related="opportunity_id.partner_id",
                                 store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="opportunity_id.planned_revenue", readonly=True)
    remarks = fields.Text('Remarks')
    ref_id = fields.Many2one('plan.action', 'Plan of Action', readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="ref_id.user_id", readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="ref_id.department_id", readonly=True)


class action_points_line(models.Model):
    _name = 'action.points.line'
    _description = 'Action Points Line'
    _order = "id desc"

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_director')
        res = super(action_points_line, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                           context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            if group_id not in user_group_id:
                doc = etree.XML(res['arch'])
                list1 = ['completion_date', 'action_point']
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('readonly', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    completion_date = fields.Date('Completion Date')
    action_point = fields.Text('Actions to be taken')
    status = fields.Selection([('Pending', 'Pending'), ('Done', 'Done')], 'Status', default='Pending')
    remarks = fields.Text('Remarks')
    ref_id = fields.Many2one('plan.action', 'Plan of Action', readonly=True)


class plan_action(models.Model):
    _name = 'plan.action'
    _inherit = ['mail.thread']
    _description = 'Plan of Action'
    _rec_name = "review_date"

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_director')
        res = super(plan_action, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                           context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            if group_id not in user_group_id:
                doc = etree.XML(res['arch'])
                list1 = ['user_id', 'department_id', 'review_date', 'plan_opportunities_line',
                         'action_points_line.completion_date', 'action_points_line.action_point']
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('readonly', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    user_id = fields.Many2one('res.users', 'Fields SalesPerson', required=False)
    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=False)
    create_uid = fields.Many2one('res.users', 'Created User', readonly=True)
    review_date = fields.Date('Review Date')
    action_points = fields.Text('Action Points')
    # cc_ids = fields.Many2many('hr.employee', 'action_plan_id', 'action_id', 'employee_id', 'CC IDs')
    plan_opportunities_line = fields.One2many('plan.opportunities.line', 'ref_id', 'Plan Opportunities Line')
    action_points_line = fields.One2many('action.points.line', 'ref_id', 'Action Points Line')

    @api.multi
    def send_mail(self):
        '''
        This function opens a window to compose an email, with the plan of action template message loaded by default
        '''
        ctx = dict(self._context)
        ctx["name"] = ''
        partner_ids = []
        if self.user_id:
            ctx["name"] = self.user_id.name
            partner_ids.append(self.user_id.partner_id.id)
        if self.department_id:
            ctx["name"] = self.department_id.manager_id.name
            partner_ids.append(self.department_id.manager_id.user_id.partner_id.id)

        body_html = '<p>Dear %s,</p><p/>' % (ctx["name"])
        body_html += '<p>Please find the action points from the Review dated %s ' \
                     'for your reference and action.</p>' % (self.review_date)

        body_html += '<table cellpadding="2" border="1">'
        body_html += '<tbody> <tr bgcolor="#D3D3D3"> ' \
                     '<td style="text-align: center;" colspan="2"> <strong>Action Points</strong></td> ' \
                     '<td style="text-align: center;" colspan="2"><strong>Completion Date</strong></td> </tr>'
        for line in self.action_points_line:
            '''action_point = ''
            if line.action_point:
                for words in line.action_point.split('.'):
                    action_point += '<p>%s</p></n>'% (words)'''
            print '\n action_point', action_point
            body_html += '<tr> <td style="text-align: center;" colspan="2"> %s </td>' % (line.action_point)
            body_html += '<td style="text-align: center;" colspan="2"> %s </td> </tr>' % (line.completion_date)
        body_html += '</tbody></table>'
        body_html += '<p> <br/><br/><br/><br/><br/></p> <p><strong> Regards,</strong><br></p>' \
                     '<p><strong> GSS - Team.</strong><br></p><p><br></p>'
        compose_form_id = self.env.ref('crm_dashboard_jmr.view_mail_compose_wizard_form').id
        ctx.update({
            # 'default_model': 'plan.action',
            'default_body': body_html,
            'default_subject': 'Review Action Points | ' + str(self.review_date),
            # 'default_res_id': self.id,
            # 'default_use_template': bool(template_id),
            # 'default_template_id': template_id,
            'default_to_ids': partner_ids,
        })

        self.state = 'Sent'
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.wizard',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'res_id': False,
            'context': ctx,
        }


class mail_compose_wizard(models.Model):
    _name = 'mail.compose.wizard'
    _inherit = ['mail.thread']
    _description = 'Mail Compose Wizard'

    subject = fields.Char('Subject', required="1")
    to_ids = fields.Many2many('res.partner', 'mail_compose_partner_to', 'partner_id', 'mail_id', "To Ids")
    cc_ids = fields.Many2many('res.partner', 'mail_compose_partner_cc', 'partner_id', 'mail_id', "CC Ids")
    body = fields.Html('Body')
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")


    @api.multi
    def send_mail(self):
        email_to = ''
        email_cc = ''
        attachments = []
        if self.to_ids:
            for partner in self.to_ids:
                email_to += partner.email + ','
        if self.cc_ids:
            for partner in self.cc_ids:
                email_cc += partner.email + ','
        if self.attachment_ids:
            for attachment_id in self.attachment_ids:
                attachments.append(attachment_id.id)
        mail_id = self.env['mail.mail'].create({
            'email_from': 'omm.gss@jmrinfotech.com',
            'email_to': email_to,
            'email_cc': email_cc,
            'subject': self.subject,
            'body_html': self.body,
            'attachment_ids': [(6, 0, attachments)],
            'model': self._name,
            'res_id': self.id,
            'auto_delete': False,
        })
        self.pool.get('mail.mail').send(self._cr, self._uid, [mail_id.id], context=self._context)
