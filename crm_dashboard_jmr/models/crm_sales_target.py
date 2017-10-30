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

from openerp import models, fields, api, _
from datetime import datetime


class crm_leads_achieved(models.Model):
    _name = 'crm.leads.achieved'
    _description = 'CRM Leads Achieved'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead')
    partner_id = fields.Many2one('res.partner', 'Customer Name', readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency ID', readonly=True)
    name = fields.Char('Opportunity Name', readonly=True)
    closed_won_date = fields.Date('Close/won date', store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit')
    department_product_ids = fields.Many2many('department.product', 'leads_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area')
    ref_id = fields.Many2one('crm.sales.target', 'Reference')


class crm_bu_target(models.Model):
    _name = 'crm.bu.target'
    _description = 'CRM BU Target'
    _order = "id desc"
    _rec_name = "department_id"

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', readonly=True)
    revenue_target = fields.Float('Target', readonly=True)
    revenue_achieved = fields.Float('Achievement', readonly=True)
    percentage = fields.Float('Percentage %', readonly=True)
    ref_id = fields.Many2one('crm.sales.target', 'Reference', readonly=True)


class sales_target(models.Model):
    _name = 'crm.sales.target'
    _inherit = ['mail.thread']
    _description = 'CRM Sales Target'
    _rec_name = "sales_target_user"

    department_id = fields.Many2one('hr.department', 'Business Unit')
    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    user_id = fields.Many2one('res.users', 'Created User', default=lambda self: self.env.user)
    revenue_target = fields.Float('Revenue Target', related='sales_target_user.revenue_target',
                                  store=True, readonly=True)
    bu_target_ids = fields.One2many('crm.bu.target', 'ref_id', 'BU Wise Target', readonly=True)
    leads_achieved = fields.One2many('crm.leads.achieved', 'ref_id', 'Achievement Breakup', readonly=True)
    revenue_achieved = fields.Float(' Revenue Achievement', readonly=True)
    percentage = fields.Float('Percentage %', readonly=True)
    date = fields.Date('Date', readonly=True, default=lambda self: fields.datetime.now())
    color = fields.Integer('Color', default=6)
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env['res.company']._company_default_get('sales_target'))

    _sql_constraints = {('sales_target_user_uniq', 'unique(sales_target_user)', ' For this user already sales target created.')}

    @api.model
    def sales_target(self):
        selfObj = self.env['crm.sales.target']
        crmLeadObj = self.env['crm.lead']
        leads_achievedObj = self.env['crm.leads.achieved']
        bu_targerObj = self.env['crm.bu.target']
        manager_relationObj = self.env['manager.users.relation']
        stage_id = ''
        stage_ids = self.env['crm.case.stage'].search([('probability', '=', 100.0)])[0]
        if stage_ids:
            stage_id = stage_ids.id
        saleperson_target_ids = self.env['saleperson.target'].search([('manager_user_relation_id', '!=', False)])
        for fields_user in saleperson_target_ids:
            bu_target = {}
            target_user = []
            revenue_achieved = 0.0
            sales_target = selfObj.search([('sales_target_user', '=', fields_user.id)])

            if not sales_target:
                sales_target = selfObj.create({'sales_target_user': fields_user.id})
            if sales_target.sales_target_user.manager_user_relation_id.user_id:
                sales_target.sales_manager = sales_target.sales_target_user.manager_user_relation_id.user_id.id
            saleperson_hierarchy = manager_relationObj.search([('user_id', '=', sales_target.sales_target_user.user_id.id)])
            if saleperson_hierarchy:
                saleperson_dept_target_line = saleperson_hierarchy[0].saleperson_dept_target_line
                for sales_person in saleperson_hierarchy[0].saleperson_target_line:
                    target_user.append(sales_person)
            else:
                saleperson_dept_target_line = fields_user.manager_user_relation_id.saleperson_dept_target_line
                target_user.append(sales_target.sales_target_user)
            lead_ids = []
            for user in target_user:
                start_date = user.start_date
                end_date = user.end_date
                for dept in saleperson_dept_target_line:
                    dept_key = dept.department_id.id
                    if dept_key not in bu_target:
                        bu_target[dept_key] = [dept.revenue_target, 0]
                domain = [('user_id', '=', user.user_id.id), ('closed_won_date', '>=', start_date),
                          ('closed_won_date', '<=', end_date), ('stage_id', '=', stage_id)]
                crm_ids = crmLeadObj.search(domain)

                for crm_id in crm_ids:
                    lead_ids.append(crm_id.id)
                    if crm_id.department_id.parent_id.parent_id:
                        key = crm_id.department_id.parent_id.id
                    else:
                        key = crm_id.department_id.id
                    if key in bu_target:
                        bu_target[key][1] += crm_id.planned_revenue
                    else:
                        bu_target[key] = [0, crm_id.planned_revenue]
                    lead_id = leads_achievedObj.search([('lead_id', '=', crm_id.id), ('ref_id', '=', sales_target.id)])
                    department_product_ids = []
                    for product_id in crm_id.department_product_ids:
                        department_product_ids.append(product_id.id)


                    if not lead_id:
                        leads_achievedObj.create({'lead_id': crm_id.id,
                                                  'name': crm_id.name,
                                                  'partner_id': crm_id.partner_id.id,
                                                  'planned_revenue': crm_id.planned_revenue,
                                                  'currency_id': crm_id.currency_id.id or False,
                                                  'closed_won_date': crm_id.closed_won_date,
                                                  'user_id': crm_id.user_id.id,
                                                  'department_id': crm_id.department_id.id,
                                                  'department_product_ids': [(6, 0, department_product_ids)],
                                                  'ref_id': sales_target.id,
                                                  })
                    else:
                        lead_id.name = crm_id.name
                        lead_id.partner_id = crm_id.partner_id.id
                        lead_id.planned_revenue = crm_id.planned_revenue
                        lead_id.currency_id = crm_id.currency_id.id or False
                        lead_id.closed_won_date = crm_id.closed_won_date
                        lead_id.user_id = crm_id.user_id.id
                        lead_id.department_id = crm_id.department_id.id
                        lead_id.department_product_ids = [(6, 0, department_product_ids)]
                    department_product_ids[:] = []
                    revenue_achieved += crm_id.planned_revenue
            current_leads_achieved_ids = [lead_achieved.id for lead_achieved in leads_achievedObj.search([
                ('lead_id', 'in', lead_ids), ('ref_id', '=', sales_target.id)])]
            total_leads_achieved_ids = [leads_achieved.id for leads_achieved in leads_achievedObj.search([
                ('ref_id', '=', sales_target.id)])]
            unlink_ids = list(set(total_leads_achieved_ids) - set(current_leads_achieved_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.leads.achieved').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            current_leads_achieved_ids[:] = []
            total_leads_achieved_ids[:] = []
            lead_ids[:] = []

            sales_target.revenue_achieved = revenue_achieved
            if not sales_target.revenue_target == 0:
                sales_target.percentage = round(float(sales_target.revenue_achieved) * 100 / sales_target.revenue_target, 2)
            for bu in bu_target:
                percentage = 0.0
                bu_id = bu_targerObj.search([('department_id', '=', bu), ('ref_id', '=', sales_target.id)])
                revenue_target = bu_target[bu][0]
                revenue_achieved = bu_target[bu][1]
                if not revenue_target == 0:
                    percentage = round(float(revenue_achieved) * 100 / revenue_target, 2)
                if bu_id:
                    bu_id.revenue_target = revenue_target
                    bu_id.revenue_achieved = revenue_achieved
                    bu_id.percentage = percentage
                else:
                    bu_targerObj.create({'department_id': bu,
                                         'revenue_target': bu_target[bu][0],
                                         'revenue_achieved': bu_target[bu][1],
                                         'percentage': percentage,
                                         'ref_id': sales_target.id})
            bu_target.clear()
            target_user[:] = []


class seller_bu_quarter_wise(models.Model):
    _name = 'seller.bu.quarter.wise'
    _description = 'Seller BU Quarter Wise'
    _inherit = ['mail.thread']
    _order = "id desc"

    @api.one
    @api.depends('ob_target', 'ob_achieved', 'revenue_target', 'revenue_achieved')
    def _compute_percentage(self):
        if self.ob_target:
            self.ob_percentage = round(float(self.ob_achieved) * 100 / self.ob_target, 2)
        else:
            self.ob_percentage = 0
        if self.revenue_target:
            self.revenue_percentage = round(float(self.revenue_achieved) * 100 / self.revenue_target, 2)
        else:
            self.revenue_percentage = 0
        self.revenue_variant = float(self.revenue_achieved) - float(self.revenue_target)
        self.ob_variant = float(self.ob_achieved) - float(self.ob_target)

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
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
    ob_ref_id = fields.Many2one('seller.order.booking', 'OB Reference', readonly=True)
    quarter_ref_id = fields.Many2one('seller.quarter.wise', 'Seller Quarter Wise', readonly=True)
    color = fields.Integer('Colour', default=6)


class seller_quarter_wise(models.Model):
    _name = 'seller.quarter.wise'
    _description = 'Seller Quarter Wise'
    _inherit = ['mail.thread']
    _order = "id desc"

    @api.one
    @api.depends('ob_target', 'ob_achieved', 'revenue_target', 'revenue_achieved')
    def _compute_percentage(self):
        if self.ob_target:
            self.ob_percentage = round(float(self.ob_achieved) * 100 / self.ob_target, 2)
        else:
            self.ob_percentage = 0
        if self.revenue_target:
            self.revenue_percentage = round(float(self.revenue_achieved) * 100 / self.revenue_target, 2)
        else:
            self.revenue_percentage = 0
        self.revenue_variant = float(self.revenue_achieved) - float(self.revenue_target)
        self.ob_variant = float(self.ob_achieved) - float(self.ob_target)

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    name = fields.Char('Quarter', readonly=True)
    ob_target = fields.Float('OB Target', readonly=False)
    ob_achieved = fields.Float('OB Achievement', readonly=False)
    ob_variant = fields.Float('OB Variant', compute=_compute_percentage, store=True, readonly=True)
    # ob_potential = fields.Float('OB Potential', readonly=True)
    ob_percentage = fields.Float('OB Achieved %', compute=_compute_percentage, store=True, readonly=True)
    revenue_target = fields.Float('Revenue Target', readonly=False)
    revenue_achieved = fields.Float('Revenue Achievement', readonly=False)
    revenue_variant = fields.Float('Revenue Variant', compute=_compute_percentage, store=True, readonly=True)
    bu_quarter_wise_ids = fields.One2many('seller.bu.quarter.wise', 'quarter_ref_id', 'BU wise Details', readonly=False)
    revenue_percentage = fields.Float('Revenue Achieved %', compute=_compute_percentage, store=True, readonly=True)
    ref_id = fields.Many2one('seller.order.booking', 'Reference', readonly=True)
    color = fields.Integer('Colour', default=6)


class seller_order_booking(models.Model):
    _name = 'seller.order.booking'
    _inherit = ['mail.thread']
    _description = 'Seller Order Booking'
    _order = "id desc"
    _rec_name = "sales_target_user"

    @api.one
    @api.depends('total_ob_target', 'total_revenue_target', 'total_revenue_achieved', 'total_ob_achieved')
    def _compute_percentage(self):
        if self.total_ob_target:
            self.ob_percentage = round(float(self.total_ob_achieved) * 100 / self.total_ob_target, 2)
        else:
            self.ob_percentage = 0
        if self.total_revenue_target:
            self.revenue_percentage = round(float(self.total_revenue_achieved) * 100 / self.total_revenue_target, 2)
        else:
            self.revenue_percentage = 0
        self.total_ob_variant = float(self.total_ob_achieved) - float(self.total_ob_target)
        self.total_revenue_variant = float(self.total_revenue_achieved) - float(self.total_revenue_target)

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    quarter_wise_ids = fields.One2many('seller.quarter.wise', 'ref_id', 'Quarter wise Details', readonly=False)
    # bu_quarter_wise_ids = fields.One2many('seller.bu.quarter.wise', 'ob_ref_id', 'BU wise Details', readonly=False)
    total_ob_achieved = fields.Float('Total OB Achievement', readonly=True)
    total_ob_target = fields.Float('Total OB Target', readonly=True)
    total_ob_variant = fields.Float('OB Variant', compute=_compute_percentage, store=True, readonly=True)
    total_revenue_achieved = fields.Float('Total Revenue Achievement', readonly=True)
    total_revenue_target = fields.Float('Total Revenue Target', readonly=True)
    total_revenue_variant = fields.Float('Revenue Variant', compute=_compute_percentage, store=True, readonly=True)
    ob_percentage = fields.Float('OB Achievement %', compute=_compute_percentage, store=True, readonly=True)
    revenue_percentage = fields.Float('Revenue Achievement %', compute=_compute_percentage, store=True, readonly=True)
    color = fields.Integer('Colour', default=6)
    # leads_achieved = fields.One2many('bu.leads.achieved', 'ref_id', 'BU Achievement Breakup', readonly=True)

    @api.model
    def sellers_ob_targets(self):
        import datetime
        selfObj = self.env['seller.order.booking']
        quarterObj = self.env['seller.quarter.wise']
        bu_quarterObj = self.env['seller.bu.quarter.wise']
        saleperson_target_ids = self.env['saleperson.target'].search([('manager_user_relation_id', '!=', False)])
        for fields_user in saleperson_target_ids:
            bu_target = []
            seller_ob_achieved = 0.0
            seller_revenue_achieved = 0.0
            seller_ob_target = 0.0
            seller_revenue_target = 0.0
            current_date = datetime.date.today()
            fiscalyear_id = None
            fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                    ('date_stop', '>=', current_date)])
            if fiscalyear_ids:
                fiscalyear_id = fiscalyear_ids[0].id
            sellers_target = selfObj.search([('sales_target_user', '=', fields_user.id)])
            if not sellers_target:
                sellers_target = selfObj.create({'sales_target_user': fields_user.id,
                                                 'fiscalyear_id': fiscalyear_id})
            saleperson_dept_target_line = fields_user.manager_user_relation_id.saleperson_dept_target_line
            for dept in saleperson_dept_target_line:
                dept_id = dept.department_id.id
                if dept_id not in bu_target:
                    bu_target.append(dept_id)

            quarter_lines = ['Quarter - 4', 'Quarter - 3', 'Quarter - 2', 'Quarter - 1']
            # quarter_wise_id = None
            for quarter in quarter_lines:
                quarter_wise_id = quarterObj.search([('name', '=', quarter), ('ref_id', '=', sellers_target.id)])
                if not quarter_wise_id:
                    quarter_wise_id = quarterObj.create({'name': quarter,
                                       'sales_target_user': sellers_target.sales_target_user.id,
                                       'sales_manager': sellers_target.sales_manager.id,
                                       'ref_id': sellers_target.id,
                                       })
                else:
                    quarter_wise_id.sales_manager = sellers_target.sales_manager.id

                for bu in bu_target:
                    bu_quarter_wise_id = bu_quarterObj.search([('quarter_ref_id', '=', quarter_wise_id.id),
                                                               ('department_id', '=', bu)])
                    if not bu_quarter_wise_id:
                        bu_quarterObj.create({'quarter_ref_id': quarter_wise_id.id,
                                           'department_id': bu,
                                           'sales_target_user': sellers_target.sales_target_user.id,
                                           'sales_manager': sellers_target.sales_manager.id,
                                           'ob_ref_id': sellers_target.id,
                                           })
                    else:
                        quarter_wise_id.sales_manager = sellers_target.sales_manager.id
            unlink_ids = [quarter_id.id for quarter_id in quarterObj.search([('ref_id', '=', False)])]
            for unlink_id in unlink_ids:
                self.pool.get('seller.quarter.wise').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []

            if sellers_target.sales_target_user.manager_user_relation_id.user_id:
                sellers_target.sales_manager = sellers_target.sales_target_user.manager_user_relation_id.user_id.id
            year1 = datetime.datetime.strptime(sellers_target.fiscalyear_id.date_start, "%Y-%m-%d").year
            year2 = datetime.datetime.strptime(sellers_target.fiscalyear_id.date_stop, "%Y-%m-%d").year
            q1_start_date = str(year1) + '-' + '04-01'
            q1_end_date = str(year1) + '-' + '06-30'
            q2_start_date = str(year1) + '-' + '07-01'
            q2_end_date = str(year1) + '-' + '09-30'
            q3_start_date = str(year1) + '-' + '10-01'
            q3_end_date = str(year1) + '-' + '12-31'
            q4_start_date = str(year2) + '-' + '01-01'
            q4_end_date = str(year2) + '-' + '03-31'
            for quarter in sellers_target.quarter_wise_ids:
                seller_ob_achieved += quarter.ob_achieved
                seller_revenue_achieved += quarter.revenue_achieved
                seller_ob_target += quarter.ob_target
                seller_revenue_target += quarter.revenue_target
            sellers_target.total_ob_achieved = seller_ob_achieved
            sellers_target.total_revenue_achieved = seller_revenue_achieved
            sellers_target.total_ob_target = seller_ob_target
            sellers_target.total_revenue_target = seller_revenue_target
