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
import datetime


class hr_department(models.Model):
    _inherit = "hr.department"

    parent = fields.Boolean('Is Parent?')

class bu_lead_achieved(models.Model):
    _name = 'bu.leads.achieved'
    _description = 'BU Leads Achieved'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead')
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    closed_won_date = fields.Date('Close/won date', related="lead_id.closed_won_date", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_achievements_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('bu.achievement', 'Reference', readonly=True)


class bu_achievement(models.Model):
    _name = 'bu.achievement'
    _inherit = ['mail.thread']
    _description = 'BU Achievement'
    _order = "id desc"
    _rec_name = "department_id"

    @api.one
    @api.depends('revenue_achieved', 'target', )
    def _compute_percentage(self):
        if self.target:
            self.percentage = round(float(self.revenue_achieved) * 100 / self.target, 2)
            self.variant = round(self.revenue_achieved - self.target, 2)
        else:
            self.percentage = 0
            self.variant = 0

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True, required=True)
    target = fields.Float('Revenue Target', readonly=False)
    revenue_achieved = fields.Float(' Revenue Achievement', readonly=True)
    variant = fields.Float(' Variant', compute=_compute_percentage, store=True, readonly=True)
    percentage = fields.Float('Percentage %', compute=_compute_percentage, store=True, readonly=True)
    leads_achieved = fields.One2many('bu.leads.achieved', 'ref_id', 'BU Achievement Breakup', readonly=True)

    @api.model
    def bu_target(self):
        bu_target = {}
        crm_total_ids = []
        current_date = datetime.date.today().month
        month = datetime.date.today().month
        year = datetime.date.today().year
        l1 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
        l2 = [1, 2, 3]
        if month in l1:
            start_date = str(year) + '_' + '04_01'
            end_date = str(int(year) + 1) + '_' + '03_31'
        else:
            start_date = str(int(year) - 1) + '_' + '04_01'
            end_date = str(year) + '_' + '03_31'
        selfObj = self.env['bu.achievement']
        crmLeadObj = self.env['crm.lead']
        leads_achievedObj = self.env['bu.leads.achieved']
        stage_id = ''
        stage_ids = self.env['crm.case.stage'].search([('probability', '=', 100.0)])[0]
        if stage_ids:
            stage_id = stage_ids.id
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        bu_records = []
        for bu in bu_ids:
            domain = [('department_id', '=', bu.id), ('closed_won_date', '>=', start_date),
                      ('closed_won_date', '<=', end_date), ('stage_id', '=', stage_id)]

            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                if bu_child:
                    bu_id = bu_child[0].id
            else:
                bu_id = bu.id
            if bu_id not in bu_target:
                bu_target[bu_id] = 0.0
            bu_records.append(bu_id)
            bu_achievement_ids = selfObj.search([('department_id', '=', bu_id)])
            if not bu_achievement_ids:
                bu_achievement_ids = selfObj.create({'department_id': bu_id})
            crm_ids = crmLeadObj.search(domain)
            for record in crm_ids:
                crm_total_ids.append(record.id)
                bu_target[bu_id] += record.planned_revenue
                bu_leads_achieved = leads_achievedObj.search([('lead_id', '=', record.id),
                                                              ('ref_id', '=', bu_achievement_ids.id)])
                if not bu_leads_achieved:
                    bu_leads_achieved.create({'lead_id': record.id,
                                              'ref_id': bu_achievement_ids.id,
                                              })
            bu_achievement_ids.revenue_achieved = bu_target[bu_id]

        # Unlink process for previous closures #

        leads_achieved_ids = [leads_achieved.id for leads_achieved in leads_achievedObj.search([
            ('lead_id', 'in', crm_total_ids)])]

        total_leads_achieved_ids = [leads_achieved.id for leads_achieved in leads_achievedObj.search([
            ('id', '!=', False)])]

        unlink_ids = list(set(total_leads_achieved_ids) - set(leads_achieved_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.leads.achieved').unlink(self._cr, self._uid, unlink_id, self._context)

        # Unlink process for BU records #

        bu_ids = [bu_record.id for bu_record in selfObj.search([('department_id', 'in', bu_records)])]

        total_bu_ids = [bu_record.id for bu_record in selfObj.search([('id', '!=', False)])]

        unlink_bu_ids = list(set(total_bu_ids) - set(bu_ids))

        for unlink_id in unlink_bu_ids:
            self.pool.get('bu.achievement').unlink(self._cr, self._uid, unlink_id, self._context)


class bu_quarter_wise(models.Model):
    _name = 'bu.quarter.wise'
    _description = 'BU Quarter Wise'
    _order = "id desc"

    @api.one
    @api.depends('ob_target', 'ob_achieved', 'revenue_target', 'revenue_achieved')
    def _compute_percentage(self):
        if self.ob_target:
            self.ob_percentage = round(float(self.ob_achieved) * 100 / self.ob_target, 2)
        else:
            self.ob_percentage = 0
        self.ob_variant =  float(self.ob_achieved) - float(self.ob_target)
        if self.revenue_target:
            self.revenue_percentage = round(float(self.revenue_achieved) * 100 / self.revenue_target, 2)

        else:
            self.revenue_percentage = 0
        self.revenue_variant = float(self.revenue_achieved) - float(self.revenue_target)

    name = fields.Char('Quarter', readonly=True)
    ob_target = fields.Float('OB Target', readonly=False)
    ob_achieved = fields.Float('OB Achievement', readonly=False)
    ob_variant = fields.Float('OB Variant', compute=_compute_percentage, store=True, readonly=True)
    # ob_potential = fields.Float('OB Potential', readonly=True)
    ob_percentage = fields.Float('OB Achieved %', compute=_compute_percentage, store=True, readonly=True)
    revenue_target = fields.Float('Revenue Target', readonly=False)
    revenue_achieved = fields.Float('Revenue Achievement', readonly=False)
    revenue_variant = fields.Float('Revenue Variant', compute=_compute_percentage, store=True, readonly=True)
    revenue_percentage = fields.Float('Revenue Achieved %', compute=_compute_percentage, store=True, readonly=True)
    ref_id = fields.Many2one('bu.order.booking', 'Reference', readonly=True)


class bu_order_booking(models.Model):
    _name = 'bu.order.booking'
    _inherit = ['mail.thread']
    _description = 'BU Order Booking'
    _order = "id desc"
    _rec_name = "department_id"

    @api.one
    @api.depends('total_ob_target', 'total_revenue_target', 'total_revenue_achieved', 'total_ob_achieved')
    def _compute_percentage(self):
        if self.total_ob_target:
            self.ob_percentage = round(float(self.total_ob_achieved) * 100 / self.total_ob_target, 2)
        else:
            self.ob_percentage = 0
        self.total_ob_variant = float(self.total_ob_achieved) - float(self.total_ob_target)
        if self.total_revenue_target:
            self.revenue_percentage = round(float(self.total_revenue_achieved) * 100 / self.total_revenue_target, 2)
        else:
            self.revenue_percentage = 0
        self.total_revenue_variant = float(self.total_revenue_achieved) - float(self.total_revenue_target)

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True, required=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    quarter_wise_ids = fields.One2many('bu.quarter.wise', 'ref_id', 'Quarter wise Details', readonly=False)
    # total_ob_potential = fields.Float('Total OB Potential', readonly=True)
    total_ob_achieved = fields.Float('Total OB Achievement', readonly=True)
    total_ob_target = fields.Float('Total OB Target', readonly=True)
    total_ob_variant = fields.Float('OB Variant', compute=_compute_percentage, store=True, readonly=True)
    total_revenue_achieved = fields.Float('Total Revenue Achievement', readonly=True)
    total_revenue_target = fields.Float('Total Revenue Target', readonly=True)
    total_revenue_variant = fields.Float('Revenue Variant', compute=_compute_percentage, store=True, readonly=True)
    ob_percentage = fields.Float('OB Achieved %', compute=_compute_percentage, store=True, readonly=True)
    revenue_percentage = fields.Float('Revenue Achieved %', compute=_compute_percentage, store=True, readonly=True)
    color = fields.Integer('Colour', default=6)
    # leads_achieved = fields.One2many('bu.leads.achieved', 'ref_id', 'BU Achievement Breakup', readonly=True)


    @api.model
    def create(self, vals):
        bu_order_booking_id = super(bu_order_booking, self).create(vals)
        quarter_lines = ['Quarter - 4', 'Quarter - 3', 'Quarter - 2', 'Quarter - 1']
        for quarter in quarter_lines:
            self.env['bu.quarter.wise'].create({'name': quarter,
                                                'ref_id': bu_order_booking_id.id,
                                                })
        return bu_order_booking_id

    @api.model
    def bu_ob_targets(self):
        q1_ob_list = {}
        q2_ob_list = {}
        q3_ob_list = {}
        q4_ob_list = {}
        q1_target_list = {}
        q2_target_list = {}
        q3_target_list = {}
        q4_target_list = {}
        selfObj = self.env['bu.order.booking']
        crmLeadObj = self.env['crm.lead']
        bu_quarter_wiseObj = self.env['bu.quarter.wise']
        stage_id = ''
        stage_ids = self.env['crm.case.stage'].search([('probability', '=', 100.0)])[0]
        if stage_ids:
            stage_id = stage_ids.id
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        for bu in bu_ids:
            bu_id = None
            fiscalyear_id = None
            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                if bu_child:
                    bu_id = bu_child[0].id
            else:
                bu_id = bu.id
            bu_ob_id = selfObj.search([('department_id', '=', bu_id)])
            if not bu_ob_id:
                current_date = datetime.date.today()
                fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                        ('date_stop', '>=', current_date)])
                if fiscalyear_ids:
                    fiscalyear_id = fiscalyear_ids[0].id
                bu_ob_id = selfObj.create({'department_id': bu_id,
                                           'fiscalyear_id': fiscalyear_id})
            year1 = datetime.datetime.strptime(bu_ob_id.fiscalyear_id.date_start, "%Y-%m-%d").year
            year2 = datetime.datetime.strptime(bu_ob_id.fiscalyear_id.date_stop, "%Y-%m-%d").year
            q1_start_date = str(year1) + '-' + '04-01'
            q1_end_date = str(year1) + '-' + '06-30'
            q2_start_date = str(year1) + '-' + '07-01'
            q2_end_date = str(year1) + '-' + '09-30'
            q3_start_date = str(year1) + '-' + '10-01'
            q3_end_date = str(year1) + '-' + '12-31'
            q4_start_date = str(year2) + '-' + '01-01'
            q4_end_date = str(year2) + '-' + '03-31'
            bu_ob_achieved = 0.0
            bu_revenue_achieved = 0.0
            bu_ob_target = 0.0
            bu_revenue_target = 0.0
            if bu_ob_id:
                quarter_wise_ids = bu_ob_id.quarter_wise_ids
                for quarter in quarter_wise_ids:
                    if quarter.name == 'Quarter - 1':
                        if bu_ob_id.id not in q1_ob_list:
                            q1_ob_list[bu_ob_id.id] = 0.0
                        if bu_ob_id.id not in q1_target_list:
                            q1_target_list[bu_ob_id.id] = 0.0
                        for crm_record in crmLeadObj.search([('department_id', '=', bu.id),
                                                             ('closed_won_date', '>=', q1_start_date),
                                                             ('closed_won_date', '<=', q1_end_date),
                                                             ('stage_id', '=', stage_id)]):
                            q1_ob_list[bu_ob_id.id] += 0.0
                            q1_target_list[bu_ob_id.id] += 0.0
                        # quarter.ob_achieved = q1_ob_list[bu_ob_id.id]
                        # quarter.revenue_achieved = q1_target_list[bu_ob_id.id]
                    if quarter.name == 'Quarter - 2':
                        if bu_ob_id.id not in q2_ob_list:
                            q2_ob_list[bu_ob_id.id] = 0.0
                        if bu_ob_id.id not in q2_target_list:
                            q2_target_list[bu_ob_id.id] = 0.0
                        for crm_record in crmLeadObj.search([('department_id', '=', bu.id),
                                                             ('closed_won_date', '>=', q2_start_date),
                                                             ('closed_won_date', '<=', q2_end_date),
                                                             ('stage_id', '=', stage_id)]):
                            q2_ob_list[bu_ob_id.id] += crm_record.planned_revenue
                            q2_target_list[bu_ob_id.id] += crm_record.planned_revenue
                        # quarter.ob_achieved = 0.0
                        # quarter.revenue_achieved = 0.0
                    if quarter.name == 'Quarter - 3':
                        if bu_ob_id.id not in q3_ob_list:
                            q3_ob_list[bu_ob_id.id] = 0.0
                        if bu_ob_id.id not in q3_target_list:
                            q3_target_list[bu_ob_id.id] = 0.0
                        for crm_record in crmLeadObj.search([('department_id', '=', bu.id),
                                                             ('closed_won_date', '>=', q3_start_date),
                                                             ('closed_won_date', '<=', q3_end_date),
                                                             ('stage_id', '=', stage_id)]):
                            q3_ob_list[bu_ob_id.id] += crm_record.planned_revenue
                            q3_target_list[bu_ob_id.id] += crm_record.planned_revenue
                        # quarter.ob_achieved = 0.0
                        # quarter.revenue_achieved = 0.0
                    if quarter.name == 'Quarter - 4':
                        if bu_ob_id.id not in q4_ob_list:
                            q4_ob_list[bu_ob_id.id] = 0.0
                        if bu_ob_id.id not in q4_target_list:
                            q4_target_list[bu_ob_id.id] = 0.0
                        for crm_record in crmLeadObj.search([('department_id', '=', bu.id),
                                                             ('closed_won_date', '>=', q4_start_date),
                                                             ('closed_won_date', '<=', q4_end_date),
                                                             ('stage_id', '=', stage_id)]):
                            q4_ob_list[bu_ob_id.id] += crm_record.planned_revenue
                            q4_target_list[bu_ob_id.id] += crm_record.planned_revenue
                        # quarter.ob_achieved = 0.0
                        # quarter.revenue_achieved = 0.0
                for quarter in quarter_wise_ids:
                    bu_ob_achieved += quarter.ob_achieved
                    bu_revenue_achieved += quarter.revenue_achieved
                    bu_ob_target += quarter.ob_target
                    bu_revenue_target += quarter.revenue_target
                bu_ob_id.total_ob_achieved = bu_ob_achieved
                bu_ob_id.total_revenue_achieved = bu_revenue_achieved
                bu_ob_id.total_ob_target = bu_ob_target
                bu_ob_id.total_revenue_target = bu_revenue_target

