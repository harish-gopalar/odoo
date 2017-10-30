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

from openerp import models, fields, api, exceptions
from datetime import datetime
import time
import datetime
from datetime import timedelta


class hr_department_responsible(models.Model):
    _inherit = 'hr.department.responsible'

    start_id = fields.Integer('Start ID', default=0)
    end_id = fields.Integer('End ID', default=100)


class account_mapping(models.Model):
    _name = 'account.mapping'
    _inherit = ['mail.thread']
    _description = 'Account Mapping'
    _rec_name = "account_id"

    @api.one
    @api.depends('account_id')
    def account_details(self):
        if self.account_id:
            self.industry_id = self.account_id.industry_id.id
            self.industry_category_id = self.account_id.industry_category_id.id
        else:
            self.industry_id = False
            self.industry_category_id = False

    @api.one
    @api.depends('crm_l0', 'crm_l1', 'crm_l2', 'crm_l3', 'seller_l0', 'seller_l1',
                 'seller_l2', 'seller_l3', 'bu_l0', 'bu_l1', 'bu_l2', 'bu_l3',)
    def _delay_days_calculation(self):
        seller_l0_delay = 0
        bu_l0_delay = 0
        seller_l1_delay = 0
        bu_l1_delay = 0
        seller_l2_delay = 0
        bu_l2_delay = 0
        seller_l3_delay = 0
        bu_l3_delay = 0
        if self.crm_l0:
            crm_l0_date = datetime.datetime.strptime(self.crm_l0, "%Y-%m-%d")
            if self.seller_l0:
                seller_l0_date = datetime.datetime.strptime(self.seller_l0, "%Y-%m-%d")
                seller_l0_delay = int((crm_l0_date - seller_l0_date).days)
            if self.bu_l0:
                bu_l0_date = datetime.datetime.strptime(self.bu_l0, "%Y-%m-%d")
                bu_l0_delay = int((crm_l0_date - bu_l0_date).days)

        if self.crm_l1:
            crm_l1_date = datetime.datetime.strptime(self.crm_l1, "%Y-%m-%d")
            if self.seller_l1:
                seller_l1_date = datetime.datetime.strptime(self.seller_l1, "%Y-%m-%d")
                seller_l1_delay = int((crm_l1_date - seller_l1_date).days)
            if self.bu_l1:
                bu_l1_date = datetime.datetime.strptime(self.bu_l1, "%Y-%m-%d")
                bu_l1_delay = int((crm_l1_date - bu_l1_date).days)

        if self.crm_l2:
            crm_l2_date = datetime.datetime.strptime(self.crm_l2, "%Y-%m-%d")
            if self.seller_l2:
                seller_l2_date = datetime.datetime.strptime(self.seller_l2, "%Y-%m-%d")
                seller_l2_delay = int((crm_l2_date - seller_l2_date).days)
            if self.bu_l2:
                bu_l2_date = datetime.datetime.strptime(self.bu_l2, "%Y-%m-%d")
                bu_l2_delay = int((crm_l2_date - bu_l2_date).days)

        if self.crm_l3:
            crm_l3_date = datetime.datetime.strptime(self.crm_l3, "%Y-%m-%d")
            if self.seller_l3:
                seller_l3_date = datetime.datetime.strptime(self.seller_l3, "%Y-%m-%d")
                seller_l3_delay = int((crm_l3_date - seller_l3_date).days)
            if self.bu_l3:
                bu_l3_date = datetime.datetime.strptime(self.bu_l2, "%Y-%m-%d")
                bu_l3_delay = int((crm_l3_date - bu_l3_date).days)

        self.seller_l0_delay = seller_l0_delay
        self.bu_l0_delay = bu_l0_delay
        self.seller_l1_delay = seller_l1_delay
        self.bu_l1_delay = bu_l1_delay
        self.seller_l2_delay = seller_l2_delay
        self.bu_l2_delay = bu_l2_delay
        self.seller_l3_delay = seller_l3_delay
        self.bu_l3_delay = bu_l3_delay

    account_id = fields.Many2one('res.partner', 'Account Name', required=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', required=False)
    department_id = fields.Many2one('hr.department', 'Business Unit', required=False)
    country_id = fields.Many2one('res.country', 'Country', related="account_id.country_id", store=True, readonly=True)
    industry_id = fields.Many2one('res.industry', 'Industry', related="account_id.industry_id", store=True,
                                  readonly=True)
    industry_category_id = fields.Many2one('res.industry.category', 'Industry Category',
                                           related="account_id.industry_category_id", store=True, readonly=True)
    crm_l0 = fields.Date('CRM L0', readonly=True)
    crm_l1 = fields.Date('CRM L1', readonly=True)
    crm_l2 = fields.Date('CRM L2', readonly=True)
    crm_l3 = fields.Date('CRM L3', readonly=True)
    seller_l0 = fields.Date('Seller L0')
    seller_l1 = fields.Date('Seller L1')
    seller_l2 = fields.Date('Seller L2')
    seller_l3 = fields.Date('Seller L3')
    bu_l0 = fields.Date('BU L0')
    bu_l1 = fields.Date('BU L1')
    bu_l2 = fields.Date('BU L2')
    bu_l3 = fields.Date('BU L3')
    seller_l0_delay = fields.Integer('Seller L0 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    seller_l1_delay = fields.Integer('Seller L1 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    seller_l2_delay = fields.Integer('Seller L2 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    seller_l3_delay = fields.Integer('Seller L3 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    bu_l0_delay = fields.Integer('BU L0 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    bu_l1_delay = fields.Integer('BU L1 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    bu_l2_delay = fields.Integer('BU L2 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    bu_l3_delay = fields.Integer('BU L3 Delay', compute='_delay_days_calculation', store=True, readonly=True)
    # check_level = fields.Boolean('Check Level', compute='_delay_days_calculation', store=True, readonly=True)
    # levels_of_account = fields.Selection([('L0', 'L0'), ('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')], 'Levels Of Account', related="account_id.levels_of_account", store=True, readonly=True)
    levels_of_account = fields.Selection([('L0', 'L0'), ('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')],
                                         'Levels Of Account', readonly=True)
    notes = fields.Text('Notes')
    color = fields.Integer('Colour', default=6)

    @api.model
    def run_account_mapping_schedule(self):
        update_start_id = 0
        update_end_id = 0
        hr_departmentBrw = self.env['hr.department.responsible'].search([('id', '=', 1)])
        fromId = 0
        toId = 0
        first_id = self.search([])[0].id
        last_id = self.search([])[-1].id
        if int(first_id) >= hr_departmentBrw.end_id:
            fromId = int(first_id)
            if not int(last_id) <= int(first_id) + 100:
                toId = int(first_id)
            else:
                toId = int(first_id) + 100
            update_start_id = toId
            update_end_id = toId + 100
        else:
            if int(hr_departmentBrw.end_id) == int(last_id):
                update_start_id = int(first_id)
                update_end_id = int(first_id) + 100
                fromId = hr_departmentBrw.start_id
                toId = hr_departmentBrw.end_id
            elif int(hr_departmentBrw.end_id) <= int(last_id):
                if not (hr_departmentBrw.end_id + 100) <= int(last_id):
                    update_end_id = int(last_id)
                else:
                    update_end_id = hr_departmentBrw.end_id + 100
                update_start_id = hr_departmentBrw.end_id
                fromId = hr_departmentBrw.start_id
                toId = hr_departmentBrw.end_id
            elif int(hr_departmentBrw.end_id) >= int(last_id):
                update_start_id = int(first_id)
                update_end_id = int(first_id) + 100
                fromId = hr_departmentBrw.start_id
                toId = int(last_id)
            else:
                pass
        print '\n from to ids ', fromId, toId
        partnerEnv = self.env['res.partner']
        current_date = time.strftime("%Y-%m-%d")
        accountMapBrws = self.search([('id', '>=', fromId), ('id', '<=', toId)])
        for account_mapping_id in accountMapBrws:
            if account_mapping_id.account_id.contact_count >= 3:
                child_count = 0
                meeting_count = 0
                offerings_line_count = 0
                for child in account_mapping_id.account_id.child_ids:
                    if child.phonecall_count > 0 and child.email_count > 0:
                        child_count += 1
                    if child.meeting_count > 0:
                        meeting_count += 1
                    if child.offerings_introduce_line:
                        offerings_line_count += 1
                if child_count >= 3:
                    if meeting_count >= 3:  # 3 meetings, atleast one meeting with 3 contacts
                        if account_mapping_id.account_id.procurement_process and account_mapping_id.account_id.empanelled:
                            if offerings_line_count > 0:
                                if not account_mapping_id.levels_of_account == 'L3':
                                    account_mapping_id.levels_of_account = 'L3'
                                    account_mapping_id.crm_l3 = current_date
                            else:
                                if not account_mapping_id.levels_of_account == 'L2':
                                    account_mapping_id.levels_of_account = 'L2'
                                    account_mapping_id.crm_l2 = current_date
                        else:
                            if not account_mapping_id.levels_of_account == 'L2':
                                account_mapping_id.levels_of_account = 'L2'
                                account_mapping_id.crm_l2 = current_date
                    else:
                        if not account_mapping_id.levels_of_account == 'L1':
                            account_mapping_id.levels_of_account = 'L1'
                            account_mapping_id.crm_l1 = current_date
                else:
                    if not account_mapping_id.levels_of_account == 'L0':
                        account_mapping_id.levels_of_account = 'L0'
                        account_mapping_id.crm_l0 = current_date
            else:
                if not account_mapping_id.levels_of_account == 'L0':
                    account_mapping_id.levels_of_account = 'L0'
                    account_mapping_id.crm_l0 = current_date
        hr_departmentBrw.start_id = update_start_id
        hr_departmentBrw.end_id = update_end_id


class seller_account_mapping_line(models.Model):
    _name = 'seller.account.mapping.line'
    _inherit = ['mail.thread']
    _description = 'Seller Account Mapping Line'
    _rec_name = "name"

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    @api.one
    @api.depends('l0_target', 'l1_target', 'l2_target', 'l3_target', 'l0_achieved', 'l1_achieved', 'l2_achieved',
                 'l3_achieved')
    def _compute_percentage(self):
        if self.l0_target:
            self.l0_percentage = round(float(self.l0_achieved) * 100 / self.l0_target, 2)
        else:
            self.l0_percentage = 0
        if self.l1_target:
            self.l1_percentage = round(float(self.l1_achieved) * 100 / self.l1_target, 2)
        else:
            self.l1_percentage = 0
        if self.l2_target:
            self.l2_percentage = round(float(self.l2_achieved) * 100 / self.l2_target, 2)
        else:
            self.l2_percentage = 0
        if self.l3_target:
            self.l3_percentage = round(float(self.l3_achieved) * 100 / self.l3_target, 2)
        else:
            self.l3_percentage = 0
        self.l0_variant = float(self.l0_achieved) - float(self.l0_target)
        self.l1_variant = float(self.l1_achieved) - float(self.l1_target)
        self.l2_variant = float(self.l2_achieved) - float(self.l2_target)
        self.l3_variant = float(self.l3_achieved) - float(self.l3_target)

    name = fields.Selection(AVAILABLE_QUARTERS, 'Quarter', readonly=True)
    l0_target = fields.Integer('L0 Target', readonly=False)
    l1_target = fields.Integer('L1 Target', readonly=False)
    l2_target = fields.Integer('L2 Target', readonly=False)
    l3_target = fields.Integer('L3 Target', readonly=False)
    l0_achieved = fields.Integer('L0 Achieved', readonly=True)
    l1_achieved = fields.Integer('L1 Achieved', readonly=True)
    l2_achieved = fields.Integer('L2 Achieved', readonly=True)
    l3_achieved = fields.Integer('L3 Achieved', readonly=True)
    l0_variant = fields.Float('L0 Variant', compute=_compute_percentage, store=True, readonly=True)
    l1_variant = fields.Float('L1 Variant', compute=_compute_percentage, store=True, readonly=True)
    l2_variant = fields.Float('L2 Variant', compute=_compute_percentage, store=True, readonly=True)
    l3_variant = fields.Float('L3 Variant', compute=_compute_percentage, store=True, readonly=True)
    l0_percentage = fields.Float('L0 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l1_percentage = fields.Float('L1 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l2_percentage = fields.Float('L2 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l3_percentage = fields.Float('L3 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    ref_id = fields.Many2one('seller.account.mapping', 'Reference', readonly=True)


class seller_account_mapping(models.Model):
    _name = 'seller.account.mapping'
    _inherit = ['mail.thread']
    _description = 'Seller Account Mapping'
    _rec_name = "user_id"

    @api.one
    @api.depends('total_l0_target', 'total_l1_target', 'total_l2_target', 'total_l3_target', 'total_l0_achieved',
                 'total_l1_achieved', 'total_l2_achieved', 'total_l3_achieved', 'total_target', 'total_achieved',
                 'seller_account_mapping_line')
    def _compute_total(self):
        l0_total = 0
        l1_total = 0
        l2_total = 0
        l3_total = 0
        l0_achieved = 0
        l1_achieved = 0
        l2_achieved = 0
        l3_achieved = 0
        if self.seller_account_mapping_line:
            for line_id in self.seller_account_mapping_line:
                l0_total += line_id.l0_target
                l1_total += line_id.l1_target
                l2_total += line_id.l2_target
                l3_total += line_id.l3_target
                l0_achieved += line_id.l0_achieved
                l1_achieved += line_id.l1_achieved
                l2_achieved += line_id.l2_achieved
                l3_achieved += line_id.l3_achieved
        self.total_l0_target = l0_total
        self.total_l1_target = l1_total
        self.total_l2_target = l2_total
        self.total_l3_target = l3_total
        self.total_l0_achieved = l0_achieved
        self.total_l1_achieved = l1_achieved
        self.total_l2_achieved = l2_achieved
        self.total_l3_achieved = l3_achieved
        self.total_target = l0_total + l1_total + l2_total + l3_total
        self.total_achieved = l0_achieved + l1_achieved + l2_achieved + l3_achieved

        if self.total_l0_target:
            self.total_l0_percentage = round(float(self.total_l0_achieved) * 100 / self.total_l0_target, 2)
        else:
            self.total_l0_percentage = 0
        if self.total_l1_target:
            self.total_l1_percentage = round(float(self.total_l1_achieved) * 100 / self.total_l1_target, 2)
        else:
            self.total_l1_percentage = 0
        if self.total_l2_target:
            self.total_l2_percentage = round(float(self.total_l2_achieved) * 100 / self.total_l2_target, 2)
        else:
            self.total_l2_percentage = 0
        if self.total_l3_target:
            self.total_l3_percentage = round(float(self.total_l3_achieved) * 100 / self.total_l3_target, 2)
        else:
            self.total_l3_percentage = 0
        if self.total_target:
            self.total_percentage = round(float(self.total_achieved) * 100 / self.total_target, 2)
        else:
            self.total_percentage = 0
        self.total_l0_variant = float(self.total_l0_achieved) - float(self.total_l0_target)
        self.total_l1_variant = float(self.total_l1_achieved) - float(self.total_l1_target)
        self.total_l2_variant = float(self.total_l2_achieved) - float(self.total_l2_target)
        self.total_l3_variant = float(self.total_l3_achieved) - float(self.total_l3_target)
        self.total_variant = float(self.total_achieved) - float(self.total_target)

    user_id = fields.Many2one('res.users', 'Fields SalesPerson', required=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    country_ids = fields.Many2many('res.country', "employee_country_rel", "user_d", "country_id", readonly=False)
    notes = fields.Text('Notes')
    total_target = fields.Integer('Total Target', compute=_compute_total, store=True, readonly=True)
    total_achieved = fields.Integer('Total Achievement', compute=_compute_total, store=True, readonly=True)
    total_variant = fields.Float('Total Variant', compute=_compute_total, store=True, readonly=True)
    total_percentage = fields.Float('Total Achievement %', compute=_compute_total, store=True, readonly=True)
    seller_account_mapping_line = fields.One2many('seller.account.mapping.line', 'ref_id',
                                                  'Seller Account Mapping Line', readonly=False)
    total_l0_target = fields.Integer('L0 Target', compute=_compute_total, store=True, readonly=True)
    total_l1_target = fields.Integer('L1 Target', compute=_compute_total, store=True, readonly=True)
    total_l2_target = fields.Integer('L2 Target', compute=_compute_total, store=True, readonly=True)
    total_l3_target = fields.Integer('L3 Target', compute=_compute_total, store=True, readonly=True)
    total_l0_achieved = fields.Integer('L0 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l1_achieved = fields.Integer('L1 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l2_achieved = fields.Integer('L2 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l3_achieved = fields.Integer('L3 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l0_variant = fields.Float('Total L0 Variant', compute=_compute_total, store=True, readonly=True)
    total_l1_variant = fields.Float('Total L1 Variant', compute=_compute_total, store=True, readonly=True)
    total_l2_variant = fields.Float('Total L2 Variant', compute=_compute_total, store=True, readonly=True)
    total_l3_variant = fields.Float('Total L3 Variant', compute=_compute_total, store=True, readonly=True)
    total_l0_percentage = fields.Float('L0 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l1_percentage = fields.Float('L1 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l2_percentage = fields.Float('L2 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l3_percentage = fields.Float('L3 Achieved %', compute=_compute_total, store=True, readonly=True)
    color = fields.Integer('Colour', default=6)

    @api.multi
    def compute_seller_account_mapping(self):
        self.sudo().run_seller_account_mapping(self.user_id)

    @api.multi
    def compute_update_level(self):
        self.env['crm.user.account.target.line'].sudo().update_level(self.user_id)

    @api.model
    def run_seller_account_mapping(self, seller_id=None):
        selfObj = self.env['seller.account.mapping']
        account_mappingObj = self.env['account.mapping']
        res_usersObj = self.env['res.users']
        account_mapping_lineObj = self.env['seller.account.mapping.line']
        field_seller_ids = None
        if seller_id:
            field_seller_ids = [seller_id]
        else:
            field_seller_ids = res_usersObj.search([('sales_category', '=', 'FieldSales')])
        print '\n fields seller', field_seller_ids
        for field_user in field_seller_ids:
            total_achieved = 0
            q1_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q2_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q3_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q4_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            account_mapping_ids = account_mappingObj.search([('user_id', '=', field_user.id)])
            current_date = datetime.date.today()
            fiscalyear_id = None
            fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                    ('date_stop', '>=', current_date)])
            if fiscalyear_ids:
                fiscalyear_id = fiscalyear_ids[0]
            if fiscalyear_id:
                year1 = datetime.datetime.strptime(fiscalyear_id.date_start, "%Y-%m-%d").year
                year2 = datetime.datetime.strptime(fiscalyear_id.date_stop, "%Y-%m-%d").year
            q1_start_date = str(year1) + '-' + '04-01'
            q1_end_date = str(year1) + '-' + '06-30'
            q2_start_date = str(year1) + '-' + '07-01'
            q2_end_date = str(year1) + '-' + '09-30'
            q3_start_date = str(year1) + '-' + '10-01'
            q3_end_date = str(year1) + '-' + '12-31'
            q4_start_date = str(year2) + '-' + '01-01'
            q4_end_date = str(year2) + '-' + '03-31'
            seller_account_mapping_id = selfObj.search([('user_id', '=', field_user.id)])
            if not seller_account_mapping_id:
                seller_account_mapping_id = selfObj.create({'user_id': field_user.id,
                                                            })
            for user_id in account_mapping_ids:
                if user_id.crm_l0 and q1_start_date <= user_id.crm_l0 <= q1_end_date:
                    q1_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q1_start_date <= user_id.crm_l1 <= q1_end_date:
                    q1_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q1_start_date <= user_id.crm_l2 <= q1_end_date:
                    q1_levels['l2'] += 1
                    total_achieved += 1
                elif user_id.crm_l0 and q1_start_date <= user_id.crm_l3 <= q1_end_date:
                    q1_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q2_start_date <= user_id.crm_l0 <= q2_end_date:
                    q2_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q2_start_date <= user_id.crm_l1 <= q2_end_date:
                    q2_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q2_start_date <= user_id.crm_l2 <= q2_end_date:
                    q2_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q2_start_date <= user_id.crm_l3 <= q2_end_date:
                    q2_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q3_start_date <= user_id.crm_l0 <= q3_end_date:
                    q3_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q3_start_date <= user_id.crm_l1 <= q3_end_date:
                    q3_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q3_start_date <= user_id.crm_l2 <= q3_end_date:
                    q3_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q3_start_date <= user_id.crm_l3 <= q3_end_date:
                    q3_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q4_start_date <= user_id.crm_l0 <= q4_end_date:
                    q4_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q4_start_date <= user_id.crm_l1 <= q4_end_date:
                    q4_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q4_start_date <= user_id.crm_l2 <= q4_end_date:
                    q4_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q4_start_date <= user_id.crm_l3 <= q4_end_date:
                    q4_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
            seller_account_mapping_id.total_achieved = total_achieved
            q1_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '1'),
                                                                         ('ref_id', '=', seller_account_mapping_id.id)])
            if not q1_account_mapping_line_id:
                q1_account_mapping_line_id = account_mapping_lineObj.create({'name': '1',
                                                                             'l0_achieved': q1_levels['l0'],
                                                                             'l1_achieved': q1_levels['l1'],
                                                                             'l2_achieved': q1_levels['l2'],
                                                                             'l3_achieved': q1_levels['l3'],
                                                                             'ref_id': seller_account_mapping_id.id,
                                                                             })
            else:
                q1_account_mapping_line_id.l0_achieved = q1_levels['l0']
                q1_account_mapping_line_id.l1_achieved = q1_levels['l1']
                q1_account_mapping_line_id.l2_achieved = q1_levels['l2']
                q1_account_mapping_line_id.l3_achieved = q1_levels['l3']
            q2_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '2'),
                                                                         ('ref_id', '=', seller_account_mapping_id.id)])
            if not q2_account_mapping_line_id:
                q2_account_mapping_line_id = account_mapping_lineObj.create({'name': '2',
                                                                             'l0_achieved': q2_levels['l0'],
                                                                             'l1_achieved': q2_levels['l1'],
                                                                             'l2_achieved': q2_levels['l2'],
                                                                             'l3_achieved': q2_levels['l3'],
                                                                             'ref_id': seller_account_mapping_id.id,
                                                                             })
            else:
                q2_account_mapping_line_id.l0_achieved = q2_levels['l0']
                q2_account_mapping_line_id.l1_achieved = q2_levels['l1']
                q2_account_mapping_line_id.l2_achieved = q2_levels['l2']
                q2_account_mapping_line_id.l3_achieved = q2_levels['l3']

            q3_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '3'),
                                                                         ('ref_id', '=', seller_account_mapping_id.id)])
            if not q3_account_mapping_line_id:
                q3_account_mapping_line_id = account_mapping_lineObj.create({'name': '3',
                                                                             'l0_achieved': q3_levels['l0'],
                                                                             'l1_achieved': q3_levels['l1'],
                                                                             'l2_achieved': q3_levels['l2'],
                                                                             'l3_achieved': q3_levels['l3'],
                                                                             'ref_id': seller_account_mapping_id.id,
                                                                             })
            else:
                q3_account_mapping_line_id.l0_achieved = q3_levels['l0']
                q3_account_mapping_line_id.l1_achieved = q3_levels['l1']
                q3_account_mapping_line_id.l2_achieved = q3_levels['l2']
                q3_account_mapping_line_id.l3_achieved = q3_levels['l3']

            q4_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '4'),
                                                                         ('ref_id', '=', seller_account_mapping_id.id)])
            if not q4_account_mapping_line_id:
                q4_account_mapping_line_id = account_mapping_lineObj.create({'name': '4',
                                                                             'l0_achieved': q4_levels['l0'],
                                                                             'l1_achieved': q4_levels['l1'],
                                                                             'l2_achieved': q4_levels['l2'],
                                                                             'l3_achieved': q4_levels['l3'],
                                                                             'ref_id': seller_account_mapping_id.id,
                                                                             })
            else:
                q4_account_mapping_line_id.l0_achieved = q4_levels['l0']
                q4_account_mapping_line_id.l1_achieved = q4_levels['l1']
                q4_account_mapping_line_id.l2_achieved = q4_levels['l2']
                q4_account_mapping_line_id.l3_achieved = q4_levels['l3']

class bu_account_mapping_line(models.Model):
    _name = 'bu.account.mapping.line'
    _inherit = ['mail.thread']
    _description = 'BU Account Mapping Line'
    _rec_name = "name"

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    @api.one
    @api.depends('l0_target', 'l1_target', 'l2_target', 'l3_target', 'l0_achieved', 'l1_achieved', 'l2_achieved',
                 'l3_achieved')
    def _compute_percentage(self):
        if self.l0_target:
            self.l0_percentage = round(float(self.l0_achieved) * 100 / self.l0_target, 2)
        else:
            self.l0_percentage = 0
        if self.l1_target:
            self.l1_percentage = round(float(self.l1_achieved) * 100 / self.l1_target, 2)
        else:
            self.l1_percentage = 0
        if self.l2_target:
            self.l2_percentage = round(float(self.l2_achieved) * 100 / self.l2_target, 2)
        else:
            self.l2_percentage = 0
        if self.l3_target:
            self.l3_percentage = round(float(self.l3_achieved) * 100 / self.l3_target, 2)
        else:
            self.l3_percentage = 0
        self.l0_variant = float(self.l0_achieved) - float(self.l0_target)
        self.l1_variant = float(self.l1_achieved) - float(self.l1_target)
        self.l2_variant = float(self.l2_achieved) - float(self.l2_target)
        self.l3_variant = float(self.l3_achieved) - float(self.l3_target)

    name = fields.Selection(AVAILABLE_QUARTERS, 'Quarter', readonly=True)
    l0_target = fields.Integer('L0 Target')
    l1_target = fields.Integer('L1 Target')
    l2_target = fields.Integer('L2 Target')
    l3_target = fields.Integer('L3 Target')
    l0_achieved = fields.Integer('L0 Achieved', readonly=True)
    l1_achieved = fields.Integer('L1 Achieved', readonly=True)
    l2_achieved = fields.Integer('L2 Achieved', readonly=True)
    l3_achieved = fields.Integer('L3 Achieved', readonly=True)
    l0_variant = fields.Float('L0 Variant', compute=_compute_percentage, store=True, readonly=True)
    l1_variant = fields.Float('L1 Variant', compute=_compute_percentage, store=True, readonly=True)
    l2_variant = fields.Float('L2 Variant', compute=_compute_percentage, store=True, readonly=True)
    l3_variant = fields.Float('L3 Variant', compute=_compute_percentage, store=True, readonly=True)
    l0_percentage = fields.Float('L0 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l1_percentage = fields.Float('L1 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l2_percentage = fields.Float('L2 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    l3_percentage = fields.Float('L3 Achieved %', compute=_compute_percentage, store=True, readonly=True)
    color = fields.Integer('Colour', default=6)
    ref_id = fields.Many2one('bu.account.mapping', 'Reference', readonly=True)


class bu_account_mapping(models.Model):
    _name = 'bu.account.mapping'
    _inherit = ['mail.thread']
    _description = 'BU Account Mapping'
    _rec_name = "department_id"

    @api.one
    @api.depends('total_l0_target', 'total_l1_target', 'total_l2_target', 'total_l3_target', 'total_l0_achieved',
                 'total_l1_achieved', 'total_l2_achieved', 'total_l3_achieved', 'total_target', 'total_achieved',
                 'bu_account_mapping_line')
    def _compute_total(self):
        l0_total = 0
        l1_total = 0
        l2_total = 0
        l3_total = 0
        l0_achieved = 0
        l1_achieved = 0
        l2_achieved = 0
        l3_achieved = 0
        if self.bu_account_mapping_line:
            for line_id in self.bu_account_mapping_line:
                l0_total += line_id.l0_target
                l1_total += line_id.l1_target
                l2_total += line_id.l2_target
                l3_total += line_id.l3_target
                l0_achieved += line_id.l0_achieved
                l1_achieved += line_id.l1_achieved
                l2_achieved += line_id.l2_achieved
                l3_achieved += line_id.l3_achieved
        self.total_l0_target = l0_total
        self.total_l1_target = l1_total
        self.total_l2_target = l2_total
        self.total_l3_target = l3_total
        self.total_l0_achieved = l0_achieved
        self.total_l1_achieved = l1_achieved
        self.total_l2_achieved = l2_achieved
        self.total_l3_achieved = l3_achieved
        self.total_target = l0_total + l1_total + l2_total + l3_total
        self.total_achieved = l0_achieved + l1_achieved + l2_achieved + l3_achieved

        if self.total_l0_target:
            self.total_l0_percentage = round(float(self.total_l0_achieved) * 100 / self.total_l0_target, 2)
        else:
            self.total_l0_percentage = 0
        if self.total_l1_target:
            self.total_l1_percentage = round(float(self.total_l1_achieved) * 100 / self.total_l1_target, 2)
        else:
            self.total_l1_percentage = 0
        if self.total_l2_target:
            self.total_l2_percentage = round(float(self.total_l2_achieved) * 100 / self.total_l2_target, 2)
        else:
            self.total_l2_percentage = 0
        if self.total_l3_target:
            self.total_l3_percentage = round(float(self.total_l3_achieved) * 100 / self.total_l3_target, 2)
        else:
            self.total_l3_percentage = 0
        if self.total_target:
            self.total_percentage = round(float(self.total_achieved) * 100 / self.total_target, 2)
        else:
            self.total_percentage = 0
        self.total_l0_variant = float(self.total_l0_achieved) - float(self.total_l0_target)
        self.total_l1_variant = float(self.total_l1_achieved) - float(self.total_l1_target)
        self.total_l2_variant = float(self.total_l2_achieved) - float(self.total_l2_target)
        self.total_l3_variant = float(self.total_l3_achieved) - float(self.total_l3_target)
        self.total_variant = float(self.total_achieved) - float(self.total_target)

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    country_ids = fields.Many2many('res.country', "employee_country_rel", "user_d", "country_id", readonly=False)
    notes = fields.Text('Notes')
    total_target = fields.Integer('Total Target', compute=_compute_total, store=True, readonly=True)
    total_achieved = fields.Integer('Total Achievement', compute=_compute_total, store=True, readonly=True)
    total_variant = fields.Float('Total Variant', compute=_compute_total, store=True, readonly=True)
    total_percentage = fields.Float('Total Achievement %', compute=_compute_total, store=True, readonly=True)
    bu_account_mapping_line = fields.One2many('bu.account.mapping.line', 'ref_id',
                                              'BU Account Mapping Line', readonly=False)
    total_l0_target = fields.Integer('L0 Target', compute=_compute_total, store=True, readonly=True)
    total_l1_target = fields.Integer('L1 Target', compute=_compute_total, store=True, readonly=True)
    total_l2_target = fields.Integer('L2 Target', compute=_compute_total, store=True, readonly=True)
    total_l3_target = fields.Integer('L3 Target', compute=_compute_total, store=True, readonly=True)
    total_l0_achieved = fields.Integer('L0 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l1_achieved = fields.Integer('L1 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l2_achieved = fields.Integer('L2 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l3_achieved = fields.Integer('L3 Achieved', compute=_compute_total, store=True, readonly=True)
    total_l0_variant = fields.Float('Total L0 Variant', compute=_compute_total, store=True, readonly=True)
    total_l1_variant = fields.Float('Total L1 Variant', compute=_compute_total, store=True, readonly=True)
    total_l2_variant = fields.Float('Total L2 Variant', compute=_compute_total, store=True, readonly=True)
    total_l3_variant = fields.Float('Total L3 Variant', compute=_compute_total, store=True, readonly=True)
    total_l0_percentage = fields.Float('L0 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l1_percentage = fields.Float('L1 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l2_percentage = fields.Float('L2 Achieved %', compute=_compute_total, store=True, readonly=True)
    total_l3_percentage = fields.Float('L3 Achieved %', compute=_compute_total, store=True, readonly=True)
    color = fields.Integer('Colour', default=6)

    @api.multi
    def compute_bu_account_mapping(self):
        self.sudo().run_bu_account_mapping(self.department_id)

    @api.model
    def run_bu_account_mapping(self, department_id=None):
        selfObj = self.env['bu.account.mapping']
        account_mappingObj = self.env['account.mapping']
        res_usersObj = self.env['res.users']
        account_mapping_lineObj = self.env['bu.account.mapping.line']
        bu_list = []
        if department_id:
            bu_list.append(department_id)
        else:
            bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
            for bu in bu_ids:
                bu_id = None
                if bu.parent:
                    bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                    if bu_child:
                        bu_id = bu_child[0]
                else:
                    bu_id = bu
                bu_list.append(bu_id)
        for bu_id in bu_list:
            total_achieved = 0
            q1_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q2_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q3_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q4_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            account_mapping_ids = account_mappingObj.search([('department_id', '=', bu_id.id)])
            current_date = datetime.date.today()
            fiscalyear_id = None
            fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                    ('date_stop', '>=', current_date)])
            if fiscalyear_ids:
                fiscalyear_id = fiscalyear_ids[0]
            if fiscalyear_id:
                year1 = datetime.datetime.strptime(fiscalyear_id.date_start, "%Y-%m-%d").year
                year2 = datetime.datetime.strptime(fiscalyear_id.date_stop, "%Y-%m-%d").year
            q1_start_date = str(year1) + '-' + '04-01'
            q1_end_date = str(year1) + '-' + '06-30'
            q2_start_date = str(year1) + '-' + '07-01'
            q2_end_date = str(year1) + '-' + '09-30'
            q3_start_date = str(year1) + '-' + '10-01'
            q3_end_date = str(year1) + '-' + '12-31'
            q4_start_date = str(year2) + '-' + '01-01'
            q4_end_date = str(year2) + '-' + '03-31'
            bu_account_mapping_id = selfObj.search([('department_id', '=', bu_id.id)])
            if not bu_account_mapping_id:
                bu_account_mapping_id = selfObj.create({'department_id': bu_id.id,
                                                            })
            for user_id in account_mapping_ids:
                if user_id.crm_l0 and q1_start_date <= user_id.crm_l0 <= q1_end_date:
                    q1_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q1_start_date <= user_id.crm_l1 <= q1_end_date:
                    q1_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q1_start_date <= user_id.crm_l2 <= q1_end_date:
                    q1_levels['l2'] += 1
                    total_achieved += 1
                elif user_id.crm_l0 and q1_start_date <= user_id.crm_l3 <= q1_end_date:
                    q1_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q2_start_date <= user_id.crm_l0 <= q2_end_date:
                    q2_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q2_start_date <= user_id.crm_l1 <= q2_end_date:
                    q2_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q2_start_date <= user_id.crm_l2 <= q2_end_date:
                    q2_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q2_start_date <= user_id.crm_l3 <= q2_end_date:
                    q2_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q3_start_date <= user_id.crm_l0 <= q3_end_date:
                    q3_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q3_start_date <= user_id.crm_l1 <= q3_end_date:
                    q3_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q3_start_date <= user_id.crm_l2 <= q3_end_date:
                    q3_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q3_start_date <= user_id.crm_l3 <= q3_end_date:
                    q3_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
                if user_id.crm_l0 and q4_start_date <= user_id.crm_l0 <= q4_end_date:
                    q4_levels['l0'] += 1
                    total_achieved += 1
                elif user_id.crm_l1 and q4_start_date <= user_id.crm_l1 <= q4_end_date:
                    q4_levels['l1'] += 1
                    total_achieved += 1
                elif user_id.crm_l2 and q4_start_date <= user_id.crm_l2 <= q4_end_date:
                    q4_levels['l2'] += 1
                    total_achieved += 1
                if user_id.crm_l0 and q4_start_date <= user_id.crm_l3 <= q4_end_date:
                    q4_levels['l3'] += 1
                    total_achieved += 1
                else:
                    pass
            bu_account_mapping_id.total_achieved = total_achieved
            q1_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '1'),
                                                                         ('ref_id', '=', bu_account_mapping_id.id)])
            if not q1_account_mapping_line_id:
                q1_account_mapping_line_id = account_mapping_lineObj.create({'name': '1',
                                                                             'l0_achieved': q1_levels['l0'],
                                                                             'l1_achieved': q1_levels['l1'],
                                                                             'l2_achieved': q1_levels['l2'],
                                                                             'l3_achieved': q1_levels['l3'],
                                                                             'ref_id': bu_account_mapping_id.id,
                                                                             })
            else:
                q1_account_mapping_line_id.l0_achieved = q1_levels['l0']
                q1_account_mapping_line_id.l1_achieved = q1_levels['l1']
                q1_account_mapping_line_id.l2_achieved = q1_levels['l2']
                q1_account_mapping_line_id.l3_achieved = q1_levels['l3']
            q2_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '2'),
                                                                         ('ref_id', '=', bu_account_mapping_id.id)])
            if not q2_account_mapping_line_id:
                q2_account_mapping_line_id = account_mapping_lineObj.create({'name': '2',
                                                                             'l0_achieved': q2_levels['l0'],
                                                                             'l1_achieved': q2_levels['l1'],
                                                                             'l2_achieved': q2_levels['l2'],
                                                                             'l3_achieved': q2_levels['l3'],
                                                                             'ref_id': bu_account_mapping_id.id,
                                                                             })
            else:
                q2_account_mapping_line_id.l0_achieved = q2_levels['l0']
                q2_account_mapping_line_id.l1_achieved = q2_levels['l1']
                q2_account_mapping_line_id.l2_achieved = q2_levels['l2']
                q2_account_mapping_line_id.l3_achieved = q2_levels['l3']

            q3_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '3'),
                                                                         ('ref_id', '=', bu_account_mapping_id.id)])
            if not q3_account_mapping_line_id:
                q3_account_mapping_line_id = account_mapping_lineObj.create({'name': '3',
                                                                             'l0_achieved': q3_levels['l0'],
                                                                             'l1_achieved': q3_levels['l1'],
                                                                             'l2_achieved': q3_levels['l2'],
                                                                             'l3_achieved': q3_levels['l3'],
                                                                             'ref_id': bu_account_mapping_id.id,
                                                                             })

            else:
                q3_account_mapping_line_id.l0_achieved = q3_levels['l0']
                q3_account_mapping_line_id.l1_achieved = q3_levels['l1']
                q3_account_mapping_line_id.l2_achieved = q3_levels['l2']
                q3_account_mapping_line_id.l3_achieved = q3_levels['l3']

            q4_account_mapping_line_id = account_mapping_lineObj.search([('name', '=', '4'),
                                                                         ('ref_id', '=', bu_account_mapping_id.id)])
            if not q4_account_mapping_line_id:
                q4_account_mapping_line_id = account_mapping_lineObj.create({'name': '4',
                                                                             'l0_achieved': q4_levels['l0'],
                                                                             'l1_achieved': q4_levels['l1'],
                                                                             'l2_achieved': q4_levels['l2'],
                                                                             'l3_achieved': q4_levels['l3'],
                                                                             'ref_id': bu_account_mapping_id.id,
                                                                             })

            else:
                q4_account_mapping_line_id.l0_achieved = q4_levels['l0']
                q4_account_mapping_line_id.l1_achieved = q4_levels['l1']
                q4_account_mapping_line_id.l2_achieved = q4_levels['l2']
                q4_account_mapping_line_id.l3_achieved = q4_levels['l3']



