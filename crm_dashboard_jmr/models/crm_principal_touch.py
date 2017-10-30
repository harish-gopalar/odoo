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

from openerp import models, fields, api, exceptions, SUPERUSER_ID
from datetime import datetime
from openerp.exceptions import ValidationError
from openerp.osv.orm import setup_modifiers
from lxml import etree


class principal_departments(models.Model):
    _name = 'principal.departments'
    _description = 'Principal Departments'
    _order = "id desc"

    name = fields.Char('Principal Name', required=True)


class minutes_meeting(models.Model):
    _name = 'minutes.meeting'
    _description = 'Minutes of Meeting'
    _order = "id desc"
    _rec_name = 'date'

    date = fields.Date('Date', required=True, default=lambda self: fields.datetime.now())
    attendees = fields.Char('Attendees', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    description = fields.Text('Description', required=True)
    ref_id = fields.Many2one('principal.touch.point', 'Reference', readonly=True)


class principal_contact(models.Model):
    _name = 'principal.contact'
    _inherit = ['mail.thread']
    _description = 'Principal Contact'
    _order = "id desc"

    name = fields.Char('Principal Contact Name', required=True)
    designation = fields.Char('Designation')
    email = fields.Char('Email ID')
    phone = fields.Char('Phone No.')
    engagement = fields.Char('Engagement')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state', 'State')
    zip = fields.Char('Zip', size=24)
    country_id = fields.Many2one('res.country', 'Country/Region')
    department_id = fields.Many2one('hr.department', 'BU/Principal')
    user_id = fields.Many2one('res.users', 'Seller')
    if_other = fields.Boolean('If Other BU/Principal')
    other_bu = fields.Char('Other BU/Principal')
    meetings_count = fields.Integer('Meetings Count')
    last_meeting_date = fields.Date('Last meeting date')
    last_meeting_mom = fields.Text('Last Meeting MOM')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The Principal Contact name Should be unique!')
    ]

    @api.model
    def update_principal_meeting_details(self):
        principal_contact_ids = self.search([])
        for contact in principal_contact_ids:
            meetings_count = 0
            last_meeting_date = ''
            last_meeting_mom = ''
            user_id = False
            principal_meeting_ids = self.env['principal.touch.point'].search([('principal_contact_id', '=', contact.id)])
            meeting_ids = self.env['minutes.meeting'].search([('ref_id.principal_contact_id', '=', contact.id)])
            if principal_meeting_ids:
                if meeting_ids:
                    last_meeting_date = meeting_ids[0].date
                    user_id = meeting_ids[0].ref_id.create_uid.id
                    last_meeting_mom = str(meeting_ids[0].description).encode('utf-8')
                for principal_id in principal_meeting_ids:
                    meetings_count += len(principal_id.minutes_meeting_ids)
            contact.meetings_count = meetings_count
            contact.last_meeting_date = last_meeting_date
            contact.last_meeting_mom = last_meeting_mom
            contact.user_id = user_id


class principal_touch_point(models.Model):
    _name = 'principal.touch.point'
    _inherit = ['mail.thread']
    _description = 'Principal Touch Point Report'
    _rec_name = "principal"
    _order = "id desc"

    AVAILABLE_PRINCIPALS = [
        ('0', 'FSGBU - FC'),
        ('1', 'ITIS'),
        ('2', 'Oracle-Applications'),
        ('3', 'FSGBU - Insurance'),
        ('4', 'FSGBU - Services - Consulting'),
        ('5', 'Oracle-Database'),
        ('6', 'FSGBU - OFSSA'),
        ('7', 'Temenos'),
    ]
    AVAILABLE_FISCAL_YEARS = [
        ('1', 'FY:17-18'),
        ('2', 'FY:19-20'),
        ('3', 'FY:20-21'),
        ('4', 'FY:21-22'),
    ]

    @api.one
    @api.depends('principal_contact_id')
    def update_principal_details(self):
        if self.principal_contact_id:
            self.country_id = self.principal_contact_id.country_id.id
            self.phone = self.principal_contact_id.phone
            self.email = self.principal_contact_id.email

    @api.one
    @api.depends('create_uid')
    def _get_manager(self):
        if self.create_uid:
            employee_id = self.env['hr.employee'].search([('user_id', '=', self.create_uid.id)])
            if employee_id:
                self.reporting_manager_id = employee_id.parent_id.user_id.id
                # self.employee_department_id = employee_id.department_id.id

    @api.one
    @api.depends('minutes_meeting_ids')
    def update_last_meeting_date(self):
        if self.minutes_meeting_ids:
            self.last_meeting_date = self.minutes_meeting_ids[0].date
        else:
            pass

    @api.one
    def write(self, vals):
        principal_point = super(principal_touch_point, self).write(vals)
        if not self.minutes_meeting_ids:
            raise exceptions.ValidationError("Please fill Minutes of Meeting")
        return principal_point

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        user_filter = []
        res = super(principal_touch_point, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                        context=context, toolbar=toolbar, submenu=submenu)
        login_user_id = self.pool('res.users').browse(cr, SUPERUSER_ID, uid, context=context)
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_BU')
        bu_department_ids = self.pool('hr.department').search(cr, SUPERUSER_ID, [('parent', '=', False),
                                                              ('dept_main_category', '=', 'Non Support'),
                                                              ('manager_id.user_id', '=', login_user_id.id)])
        bdm_department_ids = self.pool('hr.department').search(cr, SUPERUSER_ID, [('parent', '=', False),
                                                              ('dept_main_category', '=', 'Non Support'),
                                                              ('bdm_ids', 'in', [login_user_id.id])])
        list1 = ['department_id']
        user_filter = []
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if login_user_id:
                if bu_department_ids:
                    user_filter = [('parent', '=', False), ('dept_main_category', '=', 'Non Support'),
                                   ('manager_id.user_id', '=', login_user_id.id)]
                elif bdm_department_ids:
                    user_filter = [('parent', '=', False), ('dept_main_category', '=', 'Non Support'),
                                   ('bdm_ids', 'in', [login_user_id.id])]
                else:
                    user_filter = [('parent', '=', False), ('dept_main_category', '=', 'Non Support')]
                doc = etree.XML(res['arch'])
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('domain', str(user_filter))
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
            if group_id in user_group_id:
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('required', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    principal = fields.Many2one('principal.departments', 'Principal')
    principal_contact = fields.Char('Principal Contact (Delete)')
    principal_contact_id = fields.Many2one('principal.contact', 'Principal Contact')
    line_business = fields.Selection(AVAILABLE_PRINCIPALS, 'Line of business')
    fiscal_year = fields.Selection(AVAILABLE_FISCAL_YEARS, 'Fiscal Year')
    sales_plan_discussed = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Sales Plan Discussed?')
    create_uid = fields.Many2one('res.users', 'Created User', readonly=True)
    is_bu = fields.Boolean('Is Business Unit')
    department_id = fields.Many2one('hr.department', 'Business Unit')
    # employee_department_id = fields.Many2one('hr.department', 'Employee BU', compute='_get_manager', store=True)
    reporting_manager_id = fields.Many2one('res.users', 'Reporting Manager', compute='_get_manager', store=True)
    meeting_frequency = fields.Selection([('Weekly', 'Weekly'), ('Fortnight', 'Fortnight'),
                                          ('Monthly', 'Monthly')], 'Meeting frequency')
    meeting_date = fields.Date('Meeting Date')
    last_meeting_date = fields.Date('Last meeting date', compute='update_last_meeting_date', store=True, readonly=True)
    next_meeting_date = fields.Date('Next meeting date')
    organised_by = fields.Many2one('res.users', 'Meeting Organised by', default=lambda self: self.env.user)
    face2face_meeting = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Face to Face meeting')
    discussed_agreed = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Discussed and agreed?')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state', 'State')
    zip = fields.Char('Zip', size=24)
    country_id = fields.Many2one('res.country', 'Country', compute='update_principal_details', store=True, readonly=False)
    phone = fields.Char('Phone/Mobile No.', compute='update_principal_details', store=True, readonly=True)
    email = fields.Char('Email ID', compute='update_principal_details', store=True, readonly=True)
    minutes_meeting_ids = fields.One2many('minutes.meeting', 'ref_id', 'Minutes of the Meeting')
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
