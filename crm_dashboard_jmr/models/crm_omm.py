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
from datetime import timedelta
from openerp.osv.orm import setup_modifiers
from lxml import etree
import calendar


class hr_department_responsible(models.Model):
    _inherit = 'hr.department.responsible'

    omm_notification_ids = fields.Many2many('hr.employee', 'omm_notification_id', 'omm_id', 'employee_id',
                                            'OMM notifications')
    omm_updates_ids = fields.Many2many('hr.employee', 'omm_updates_id', 'omm_lead_id', 'employee_id',
                                       'OMM Updates from lead: TO ids')

class public_sector_activities(models.Model):
    _name = 'public.sector.activities'
    _description = 'Customer Public Sector Activities'
    _order = "id desc"

    name = fields.Char('Activity Name', required=True)
    description = fields.Text('Description')


class oracle_products(models.Model):
    _name = 'oracle.products'
    _description = 'Oracle Products'
    _order = "id desc"

    name = fields.Char('Product Name', required=True)


class cloud_deal_contracts(models.Model):
    _name = 'cloud.deal.contracts'
    _description = 'Cloud Deal Contracts'
    _order = "id desc"

    name = fields.Char('Contract Name', required=True)

class crm_omm(models.Model):
    _name = 'crm.omm'
    _inherit = ['mail.thread']
    _description = 'Open Market Model'
    _rec_name = "opportunity_id"

    AVAILABLE_REGISTRATION_STATES = [
        ('1', 'Approved'),
        ('2', 'Extended'),
        ('3', 'Expiring'),
        ('4', 'Expired'),
        ('5', 'Declined'),
        ('6', 'Return to Partner'),
    ]

    AVAILABLE_SALES_STATES = [
        ('0', 'Assessment & Qualification'),
        ('1', 'Discovery'),
        ('2', 'Solution Development'),
        ('3', 'Solution Presentation'),
        ('4', 'Resolution'),
        ('5', 'Close'),
    ]

    AVAILABLE_STAGES = [
        ('0', 'Draft'),
        ('1', 'Approved'),
        ('2', 'OMM Submitted'),
        ('3', 'Fusion Oppty'),
        ('4', 'Rejected'),
    ]

    AVAILABLE_WIN_LOSS_REASON = [
        ('0', 'WON - Competitive Pricing'),
        ('1', 'WON - Product Fit'),
        ('2', 'WON - Relationship'),
        ('3', 'LOST - Competitor Pricing'),
        ('4', 'LOST - Competitor Product'),
        ('5', 'LOST - Competitor Relationship'),
        ('6', 'LOST - Internal Project'),
        ('7', 'LOST - Primary Reason was Serive Issue'),
        ('8', 'Closed - Alternative Oracle Solution'),
        ('9', 'Closed - Customer Not Ready / Project On Hold'),
        ('10', 'Closed - Customer Aquired'),
        ('11', 'Closed - No Business Opportunity / Poor Lead'),
    ]

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_director')
        res = super(crm_omm, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                           context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            if group_id not in user_group_id:
                doc = etree.XML(res['arch'])
                list1 = ['deal_reg_id', 'approved_omm_fusion', 'fusion_number', 'omm_sales_channel',
                         'extension_submitted', 'submitted_date', 'oracle_sales_stage', 'oracle_expiring_date',
                         'oracle_registration_status', 'oracle_opp_close_date', 'oracle_fusion_status',
                         'oracle_payment_request_status', 'oracle_win_loss_reason', 'omm_required']
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('readonly', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    @api.one
    def update_opportunities_details(self):
        oracle_product_ids = []
        if self.oracle_product_ids:
            for oracle_products_id in self.oracle_product_ids:
                oracle_product_ids.append(oracle_products_id.id)
        sector_activities_list = []
        if self.sector_activities:
            for sector_activities_id in self.sector_activities:
                sector_activities_list.append(sector_activities_id.id)
        deal_contracts_list = []
        if self.deal_contracts:
            for deal_contracts_id in self.deal_contracts:
                deal_contracts_list.append(deal_contracts_id.id)
        if self.opportunity_id:
            vals = {
                'account_id': self.account_id.id,
                'opportunity_id': self.id,
                'oracle_product_ids': [(6, 0, oracle_product_ids)],
                'sales_team': self.sales_team.id,
                'oracle_competitor': self.oracle_competitor,
                'deal_reg_id': self.deal_reg_id,
                'deal_reg_type': self.deal_reg_type,
                'approved_omm_fusion': self.approved_omm_fusion,
                'extension_submitted': self.extension_submitted,
                'extension_close_date1': self.extension_close_date1,
                'extension_close_date2': self.extension_close_date2,
                'omm_write_date': self.write_date,
                'opp_close_date': self.opp_close_date,
                'omm_date_deadline': self.date_deadline,
                'title': self.title,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'omm_street': self.street,
                'omm_street2': self.street2,
                'omm_city': self.city,
                'omm_state_id': self.state_id.id,
                'omm_zip': self.zip,
                'omm_country_id': self.country_id.id,
                'omm_region_id': self.region_id.id,
                'omm_phone': self.phone,
                'omm_email': self.email,
                'proposed_solution': self.proposed_solution,
                'detailed_opportunity': self.detailed_opportunity,
                'solution_reason': self.solution_reason,
                'department_impacted': self.department_impacted,
                'region_requirements': self.region_requirements,
                'bom_price': self.bom_price,
                'discounted_price': self.discounted_price,
                'discount': self.discount,
                'oracle_sales_manager': self.oracle_sales_manager,
                'omm_sales_channel': self.omm_sales_channel,
                'budgets_approved': self.budgets_approved,
                'direct_rfp': self.direct_rfp,
                'payment_request_status': self.payment_request_status,
                'public_sector_customer': self.public_sector_customer,
                'sector_activities': [(6, 0, sector_activities_list)],
                'cloud_deal': self.cloud_deal,
                'deal_contracts': [(6, 0, deal_contracts_list)],
                'submitted_date': self.submitted_date,
                'expiring_date': self.expiring_date,
                'registration_status': self.registration_status,
                'fusion_status': self.fusion_status,
                'fusion_number': self.fusion_number,
                'sales_stage': self.sales_stage,
                'revised_value': self.revised_value,
                'revised_reason': self.revised_reason,
                'decline_reason': self.decline_reason,
                'win_loss_reason': self.win_loss_reason,
                'revised_closure_date': self.revised_closure_date,
                'revised_date_reason': self.revised_date_reason,
                'reg_info_sales': self.reg_info_sales,
                'reg_info_sellers': self.reg_info_sellers,
                'omm_notes': self.omm_notes,
                'omm_status': self.status,
                'from_lead': True,
                'from_omm': True,
            }
            self.opportunity_id.write(vals)
        return True

    @api.one
    @api.depends('sales_stage')
    def sales_stage_changed_date(self):
        if self.sales_stage:
            self.sales_stage_updated = datetime.date.today()

    account_id = fields.Many2one('res.partner', 'Account Name', required=True)
    opportunity_id = fields.Many2one('crm.lead', 'Lead/Opportunity Name', required=True)
    opp_ref_no = fields.Char('Opportunity Reference No.', related="opportunity_id.opp_ref_no", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="opportunity_id.department_id", store=True,
                                    readonly=True)
    opp_stage = fields.Many2one('crm.case.stage', 'Opportunity Stage', related="opportunity_id.stage_id", store=True,
                                readonly=True)
    user_id = fields.Many2one('res.users', 'Seller', related="opportunity_id.user_id", store=True,
                              readonly=True)
    oracle_product_ids = fields.Many2many('oracle.products', 'omm_oracle_product',
                                          'lead_id', 'oracle_product_id', 'Products')
    sales_team = fields.Many2one('crm.case.section', 'Sales Team')
    distributor = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Distributor (VAD)')
    distributor_company = fields.Char('Distributor Company Name')
    distributor_org = fields.Char('Org Name')
    distributor_gsi = fields.Char('GSI Account Number')
    distributor_tax = fields.Char('Tax Reg Number')
    oracle_competitor = fields.Char('Oracle Competitor')
    create_uid = fields.Many2one('res.users', 'Created User', readonly=True)
    deal_reg_id = fields.Char('DealReg ID')
    status = fields.Selection(AVAILABLE_STAGES, 'Status', default='0')
    deal_reg_type = fields.Selection([('Resale', 'Resale'), ('Referral', 'Referral')], 'DealReg Type')
    approved_omm_fusion = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Approved in OMM / Fusion')
    extension_submitted = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Extension Submitted')
    extension_close_date1 = fields.Date('Extension Close Date 1')
    extension_close_date2 = fields.Date('Extension Close Date 2')

    sales_stage_updated = fields.Date('Sales Stage Updated Date', compute='sales_stage_changed_date',
                                      store=True, readonly=True)
    create_date = fields.Date('Create Date', readonly=True)
    write_date = fields.Date('Last Update Date', readonly=True)
    opp_close_date = fields.Date('JMR Opportunity Close Date')
    oracle_opp_close_date = fields.Date('Oracle Opportunity Close Date')
    date_deadline = fields.Date('Expected Closure Date')
    title = fields.Selection([('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms')], 'Title')
    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state', 'State')
    zip = fields.Char('Zip', size=24)
    country_id = fields.Many2one('res.country', 'Country', required=True)
    region_id = fields.Many2one('res.region', 'Region')
    phone = fields.Char('Phone/Mobile No.')
    email = fields.Char('Company Email ID')
    proposed_solution = fields.Char('Proposed Solution')
    detailed_opportunity = fields.Char('Detailed Opportunity Description')
    solution_reason = fields.Char('Why customer needs the solution')
    department_impacted = fields.Char('Department Impacted')
    region_requirements = fields.Char('Region Specific Requirements')
    bom_price = fields.Float('Price of BOM (USD)')
    discounted_price = fields.Float('Discounted Price (USD)')
    discount = fields.Float('Discount %')
    oracle_sales_manager = fields.Char('Oracle Sales Manager (Tagged to this opportunity)')
    omm_sales_channel = fields.Selection([('direct', 'Direct'), ('indirect', 'InDirect')], 'OMM Sales Channel')
    budgets_approved = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Budgets Approved')
    direct_rfp = fields.Selection([('Direct', 'Direct'), ('RFP', 'RFP')], 'Direct /RFP')
    payment_request_status = fields.Selection([('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'),
                                               ('Rejected', 'Rejected')], 'JMR Payment Request Status')
    oracle_payment_request_status = fields.Selection([('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'),
                                                      ('Rejected', 'Rejected')], 'Oracle Payment Request Status')
    public_sector_customer = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Customer Public Sector?')
    sector_activities = fields.Many2many('public.sector.activities', 'omm_sector_activities',
                                         'crm_omm_id', 'sector_activities_id',
                                         'Public Sector Activities ( Minimum 3 should select)')
    cloud_deal = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Cloud Deal?')
    deal_contracts = fields.Many2many('cloud.deal.contracts', 'omm_deal_contracts',
                                      'crm_omm_id', 'deal_contracts_id', 'Cloud Deal Contracts')
    submitted_date = fields.Date('Submitted date')
    expiring_date = fields.Date('JMR Expiring date')
    oracle_expiring_date = fields.Date('Oracle Expiring date')
    registration_status = fields.Selection(AVAILABLE_REGISTRATION_STATES, 'JMR Deal Registration Status')
    oracle_registration_status = fields.Selection(AVAILABLE_REGISTRATION_STATES, 'Oracle Deal Registration Status')
    fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won'),
                                      ('Closed', 'Closed')], 'JMR Fusion Opportunity Status')
    oracle_fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won'),
                                             ('Closed', 'Closed')], 'Oracle Fusion Opportunity Status')
    sales_stage = fields.Selection(AVAILABLE_SALES_STATES, 'JMR Sales Stage')
    oracle_sales_stage = fields.Selection(AVAILABLE_SALES_STATES, 'Oracle Sales Stage')
    fusion_number = fields.Char('Fusion Oppty No')
    revised_value = fields.Integer('Revised Value (USD)')
    revised_reason = fields.Char('Reason for Revised Value')
    decline_reason = fields.Char('Decline Reason')
    win_loss_reason = fields.Selection(AVAILABLE_WIN_LOSS_REASON, 'JMR Win/Loss Reason')
    oracle_win_loss_reason = fields.Selection(AVAILABLE_WIN_LOSS_REASON, 'Oracle Win/Loss Reason')
    revised_closure_date = fields.Date('Revised Closure date')
    revised_date_reason = fields.Char('Reason for Revised Closure date')
    reg_info_sales = fields.Text('Deal Registration Status Notes: Sales Support')
    reg_info_sellers = fields.Text('Deal Registration Status Notes: Seller')
    omm_notes = fields.Text('OMM Notes')
    reject_notes = fields.Text('Reason for Reject')
    approval_notes = fields.Text('Reason for Approval')
    from_lead = fields.Boolean('Is from Lead?', default=False)
    updating_check = fields.Boolean('Updating Check', default=False)
    mismatch_check = fields.Boolean('Mismatch Check', default=False)
    create_mail_sent = fields.Boolean('Check OMM Create Mail Sent', default=False)
    is_omm_mismatch = fields.Boolean('OMM Mismatch', readonly=True)
    mismatch_name = fields.Char('Mismatch Names', readonly=True)
    color = fields.Integer('Colour', default=6)

    @api.model
    def check_mismatch_omm(self):
        sales_stageObj = self.env['omm.mismatch.sales.stage']
        expiring_dateObj = self.env['omm.mismatch.expiring.date']
        opportunity_dateObj = self.env['omm.mismatch.opportunity.date']
        fusion_stageObj = self.env['omm.mismatch.fusion.status']
        sales_stage_list = []
        expiring_date_list = []
        opp_close_date_list = []
        deal_status_list = []
        fusion_status_list = []
        for omm_id in self.search([('id', '!=', False)]):
            if not omm_id.sales_stage == omm_id.oracle_sales_stage:
                sales_stage_id = sales_stageObj.search([('omm_id', '=', omm_id.id)])
                if not sales_stage_id:
                    sales_stageObj.create({'omm_id': omm_id.id})
                sales_stage_list.append(omm_id.id)

            if not omm_id.expiring_date == omm_id.oracle_expiring_date:
                expiring_date_id = expiring_dateObj.search([('omm_id', '=', omm_id.id)])
                if not expiring_date_id:
                    expiring_dateObj.create({'omm_id': omm_id.id})
                expiring_date_list.append(omm_id.id)

            if not omm_id.opp_close_date == omm_id.oracle_opp_close_date:
                opp_close_date_id = opportunity_dateObj.search([('omm_id', '=', omm_id.id)])
                if not opp_close_date_id:
                    opportunity_dateObj.create({'omm_id': omm_id.id})
                opp_close_date_list.append(omm_id.id)

            '''if not omm_id.registration_status == omm_id.oracle_registration_status:
                deal_status_id = deal_statusObj.search([('omm_id', '=', omm_id.id)])
                if not deal_status_id:
                    deal_statusObj.create({'omm_id': omm_id.id})
                deal_status_list.append(omm_id.id)'''

            if not omm_id.fusion_status == omm_id.oracle_fusion_status:
                fusion_status_id = fusion_stageObj.search([('omm_id', '=', omm_id.id)])
                if not fusion_status_id:
                    fusion_stageObj.create({'omm_id': omm_id.id})
                fusion_status_list.append(omm_id.id)

        sales_stage_ids = [sales_stage.id for sales_stage in
                           sales_stageObj.search([('omm_id', 'not in', sales_stage_list)])]

        for sales_stage_id in sales_stage_ids:
            self.pool.get('omm.mismatch.sales.stage').unlink(self._cr, self._uid, sales_stage_id, self._context)

        expiring_date_ids = [expiring_date.id for expiring_date in
                             expiring_dateObj.search([('omm_id', 'not in', expiring_date_list)])]

        for expiring_date_id in expiring_date_ids:
            self.pool.get('omm.mismatch.expiring.date').unlink(self._cr, self._uid, expiring_date_id, self._context)

        opportunity_date_ids = [opportunity_date.id
                                for opportunity_date in
                                opportunity_dateObj.search([('omm_id', 'not in', opp_close_date_list)])]

        for opportunity_date_id in opportunity_date_ids:
            self.pool.get('omm.mismatch.opportunity.date').unlink(self._cr, self._uid, opportunity_date_id, self._context)

        '''deal_status_ids = [deal_status.id for deal_status in
                           deal_statusObj.search([('omm_id', 'not in', deal_status_list)])]

        for deal_status_id in deal_status_ids:
            self.pool.get('omm.mismatch.deal.status').unlink(self._cr, self._uid, deal_status_id, self._context)'''

        fusion_status_ids = [fusion_status.id for fusion_status in
                             fusion_stageObj.search([('omm_id', 'not in', fusion_status_list)])]

        for fusion_status_id in fusion_status_ids:
            self.pool.get('omm.mismatch.fusion.status').unlink(self._cr, self._uid, fusion_status_id, self._context)

    @api.one
    def confirm(self):
        ctx = dict(self._context)
        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'omm_registration_updating_email_template')[1]
        ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
        if self.opportunity_id.user_id:
            ctx["to"] = self.opportunity_id.user_id.login or ''
        ctx["cc"] = ''
        ctx["products"] = ' '
        ctx["updates"] = 'Approved'
        ctx["changes"] = []
        ctx["changes"].append(self.approval_notes or '')
        cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
        if cc_ids.omm_notification_ids:
            for cc_id in cc_ids.omm_notification_ids:
                if cc_id.work_email:
                    ctx["cc"] += cc_id.work_email + ','
        self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, self.id, force_send=False,
                                                  raise_exception=True, context=ctx)
        self.write({'status': '1', 'updating_check': True})

    @api.one
    def omm_submitted(self):
        ctx = dict(self._context)
        if not self.deal_reg_id:
            raise exceptions.ValidationError("Please Update DealReg ID")
        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'omm_registration_submitted_email_template')[1]
        ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
        if self.opportunity_id.user_id:
            ctx["to"] = self.opportunity_id.user_id.login or ''
        ctx["cc"] = ''
        ctx["products"] = ' '
        for product in self.oracle_product_ids:
            ctx["products"] += product.name + ', '
        cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
        if cc_ids.omm_notification_ids:
            for cc_id in cc_ids.omm_notification_ids:
                if cc_id.work_email:
                    ctx["cc"] += cc_id.work_email + ','
        self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, self.id, force_send=False,
                                                  raise_exception=True, context=ctx)
        self.write({'status': '2', 'updating_check': True})

    @api.one
    def fusion_oppty_approved(self):
        ctx = dict(self._context)
        if not self.fusion_number:
            raise exceptions.ValidationError("Please Update Fusion Oppty No")
        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'omm_fusion_status_email_template')[1]
        ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
        if self.opportunity_id.user_id:
            ctx["to"] = self.opportunity_id.user_id.login or ''
        ctx["cc"] = ''
        cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
        if self.sales_stage:
            ctx["sales_stage"] = dict(self.AVAILABLE_SALES_STATES)[self.sales_stage] or ''
        if cc_ids.omm_notification_ids:
            for cc_id in cc_ids.omm_notification_ids:
                if cc_id.work_email:
                    ctx["cc"] += cc_id.work_email + ','
        self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, self.id, force_send=False,
                                                  raise_exception=True, context=ctx)
        self.write({'status': '3', 'updating_check': True})

    @api.one
    def set_draft(self):
        self.status = '0'

    @api.one
    def reject(self):
        if not self.reject_notes:
            raise exceptions.ValidationError("Please Update reason for reject")
        self.write({'status': '4', 'updating_check': True})

    @api.one
    def write(self, vals):
        ctx = dict(self._context)
        omm_id = super(crm_omm, self).write(vals)
        if not vals.get('mismatch_check'):
            template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                         'omm_registration_updating_email_template')[1]
            ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
            if self.bom_price == 0 or self.discounted_price == 0:
                raise exceptions.ValidationError("Price of BOM (USD) and Discounted Price (USD) should not be 0.0")
            if self.public_sector_customer == 'YES' and not len(self.sector_activities) >= 3:
                raise exceptions.ValidationError("Please select At least 3 Public Sector Activities")
            if not vals.get('from_lead'):
                self.update_opportunities_details()
            if not vals.get('updating_check'):
                if not vals.get('create_mail_sent'):
                    if self.opportunity_id.user_id:
                        ctx["to"] = self.opportunity_id.user_id.login or ''
                    ctx["cc"] = ''
                    ctx["updates"] = 'Following Changes happened in above account'
                    ctx["changes"] = []

                    if vals.get('registration_status'):
                        registration_status = 'JMR Deal Registration Status: ' + dict(self.AVAILABLE_REGISTRATION_STATES)[self.registration_status] or ''
                        ctx["changes"].append(registration_status)

                    if vals.get('oracle_registration_status'):
                        oracle_registration_status = 'Oracle Deal Registration Status: ' + dict(self.AVAILABLE_REGISTRATION_STATES)[self.oracle_registration_status] or ''
                        ctx["changes"].append(oracle_registration_status)

                    if vals.get('sales_stage'):
                        deal_status = 'JMR Sales Stage: ' + dict(self.AVAILABLE_SALES_STATES)[self.sales_stage] or ''
                        ctx["changes"].append(deal_status)

                    if vals.get('oracle_sales_stage'):
                        oracle_deal_status = 'Oracle Sales Stage: ' + dict(self.AVAILABLE_SALES_STATES)[self.oracle_sales_stage] or ''
                        ctx["changes"].append(oracle_deal_status)

                    if vals.get('win_loss_reason'):
                        win_loss_reason = 'Win/Loss Reason: ' + dict(self.AVAILABLE_WIN_LOSS_REASON)[self.win_loss_reason] or ''
                        ctx["changes"].append(win_loss_reason)

                    if vals.get('fusion_status'):
                        fusion_status = 'JMR Fusion Status: ' + self.fusion_status or ''
                        ctx["changes"].append(fusion_status)

                    if vals.get('oracle_fusion_status'):
                        oracle_fusion_status = 'Oracle Fusion Status: ' + self.oracle_fusion_status or ''
                        ctx["changes"].append(oracle_fusion_status)

                    if vals.get('omm_sales_channel'):
                        omm_sales_channel = 'JMR Sales Channel: ' + self.omm_sales_channel or ''
                        ctx["changes"].append(omm_sales_channel)

                    if vals.get('payment_request_status'):
                        payment_request_status = 'JMR Payment Request Status: ' + self.payment_request_status or ''
                        ctx["changes"].append(payment_request_status)

                    if vals.get('oracle_payment_request_status'):
                        oracle_payment_request_status = 'Oracle Payment Request Status: ' + self.oracle_payment_request_status or ''
                        ctx["changes"].append(oracle_payment_request_status)

                    if vals.get('opp_close_date'):
                        opp_close_date = 'Opportunity Close Date: ' + str(self.opp_close_date or '')
                        ctx["changes"].append(opp_close_date)

                    if vals.get('oracle_opp_close_date'):
                        oracle_opp_close_date = 'Oracle Opportunity Close Date: ' + str(self.oracle_opp_close_date or '')
                        ctx["changes"].append(oracle_opp_close_date)

                    if vals.get('date_deadline'):
                        date_deadline = 'Expected Closure Date: ' + str(self.date_deadline or '')
                        ctx["changes"].append(date_deadline)

                    if vals.get('expiring_date'):
                        expiring_date = 'JMR Expiring date: ' + str(self.expiring_date or '')
                        ctx["changes"].append(expiring_date)

                    if vals.get('oracle_expiring_date'):
                        oracle_expiring_date = 'Oracle Expiring date: ' + str(self.oracle_expiring_date or '')
                        ctx["changes"].append(oracle_expiring_date)

                    if vals.get('bom_price'):
                        bom_price = 'Price of BOM (USD): ' + str(self.bom_price or '')
                        ctx["changes"].append(bom_price)

                    if vals.get('discounted_price'):
                        discounted_price = 'Discounted Price (USD): ' + str(self.discounted_price or '')
                        ctx["changes"].append(discounted_price)

                    if vals.get('discounted_price'):
                        discount = 'Discount %: ' + str(self.discount or '')
                        ctx["changes"].append(discount)

                    if vals.get('distributor'):
                        distributor = 'Distributor (VAD): ' + str(self.distributor or '')
                        ctx["changes"].append(distributor)

                    if vals.get('distributor_company'):
                        distributor_company = 'Distributor Company Name: ' + str(self.distributor_company or '')
                        ctx["changes"].append(distributor_company)

                    if vals.get('distributor_org'):
                        distributor_org = 'Distributor Org Name: ' + str(self.distributor_org or '')
                        ctx["changes"].append(distributor_org)

                    if vals.get('distributor_gsi'):
                        distributor_gsi = 'GSI Account Number: ' + str(self.distributor_gsi or '')
                        ctx["changes"].append(distributor_gsi)

                    if vals.get('distributor_tax'):
                        distributor_tax = 'Tax Reg Number: ' + str(self.distributor_tax or '')
                        ctx["changes"].append(distributor_tax)

                    if vals.get('deal_reg_type'):
                        deal_reg_type = 'DealReg Type: ' + str(self.deal_reg_type or '')
                        ctx["changes"].append(deal_reg_type)

                    if vals.get('direct_rfp'):
                        direct_rfp = 'Direct /RFP: ' + self.direct_rfp or ''
                        ctx["changes"].append(direct_rfp)

                    if vals.get('budgets_approved'):
                        budgets_approved = 'Budgets Approved: ' + str(self.budgets_approved or '')
                        ctx["changes"].append(budgets_approved)

                    if vals.get('extension_submitted'):
                        extension_submitted = 'Extension Submitted: ' + str(self.extension_submitted or '')
                        ctx["changes"].append(extension_submitted)

                    if vals.get('extension_close_date1'):
                        extension_close_date1 = 'Extension Close Date 1: ' + str(self.extension_close_date1 or '')
                        ctx["changes"].append(extension_close_date1)

                    if vals.get('extension_close_date2'):
                        extension_close_date2 = 'Extension Close Date 2: ' + str(self.extension_close_date2 or '')
                        ctx["changes"].append(extension_close_date2)

                    if vals.get('submitted_date'):
                        submitted_date = 'Submitted Date: ' + str(self.submitted_date or '')
                        ctx["changes"].append(submitted_date)

                    if vals.get('oracle_sales_manager'):
                        oracle_sales_manager = 'Oracle Sales Manager (Tagged to this opportunity): ' + str(self.oracle_sales_manager or '')
                        ctx["changes"].append(oracle_sales_manager)

                    if vals.get('decline_reason'):
                        decline_reason = 'Decline Reason: ' + str(self.decline_reason or '')
                        ctx["changes"].append(decline_reason)

                    if vals.get('revised_value'):
                        revised_value = 'Revised Value: ' + str(self.revised_value or '')
                        ctx["changes"].append(revised_value)

                    if vals.get('revised_reason'):
                        revised_reason = 'Reason for Revised Value: ' + str(self.revised_reason or '')
                        ctx["changes"].append(revised_reason)

                    if vals.get('revised_closure_date'):
                        revised_closure_date = 'Revised Closure Date: ' + str(self.revised_closure_date or '')
                        ctx["changes"].append(revised_closure_date)

                    if vals.get('revised_date_reason'):
                        revised_date_reason = 'Reason for Revised Closure Date: ' + str(self.revised_date_reason or '')
                        ctx["changes"].append(revised_date_reason)

                    if vals.get('reg_info_sellers'):
                        reg_info_sellers = 'Deal Registration Status Notes: Seller: ' + str(self.reg_info_sellers or '')
                        ctx["changes"].append(reg_info_sellers)

                    if vals.get('reg_info_sales'):
                        reg_info_sales = 'Deal Registration Status Notes: Sales Support: ' + str(self.reg_info_sales or '')
                        ctx["changes"].append(reg_info_sales)

                    if vals.get('omm_notes'):
                        omm_notes = 'OMM Notes: ' + str(self.omm_notes or '')
                        ctx["changes"].append(omm_notes)

                    cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
                    if cc_ids.omm_notification_ids:
                        for cc_id in cc_ids.omm_notification_ids:
                            if cc_id.work_email:
                                ctx["cc"] += cc_id.work_email + ','
                    self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, self.id, force_send=False,
                                                              raise_exception=True, context=ctx)
            return omm_id

    @api.model
    def create(self, vals):
        ctx = dict(self._context)
        if vals.get('bom_price') == 0 or vals.get('discounted_price') == 0:
            raise exceptions.ValidationError("Price of BOM (USD) and Discounted Price (USD) should not be 0.0")
        vals['create_mail_sent'] = 'True'
        omm_id = super(crm_omm, self).create(vals)
        if omm_id.public_sector_customer == 'YES' and not len(omm_id.sector_activities) >= 3:
            raise exceptions.ValidationError("Please select At least 3 Public Sector Activities")

        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'omm_registration_email_template')[1]
        ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
        opportunity_id = vals['opportunity_id']
        if opportunity_id:
            opportunity_record = self.env['crm.lead'].search([('id', '=', opportunity_id)])
            if opportunity_record:
                opportunity_record.omm_id = omm_id
        ctx["to"] = 'a.srinivasan@jmrinfotech.com'
        ctx["cc"] = ''
        ctx["products"] = ' '
        ctx["cc"] += 'jayafar.moidu@jmrinfotech.com' + ','
        for product in omm_id.oracle_product_ids:
            ctx["products"] += product.name + ', '
        cc_ids = self.env['hr.department.responsible'].sudo().search([('id', '=', 1)])
        if cc_ids.sudo().omm_notification_ids:
            for cc_id in cc_ids.sudo().omm_notification_ids:
                if cc_id.work_email:
                    ctx["cc"] += cc_id.sudo().work_email + ','
        if omm_id.opportunity_id.user_id:
            ctx["cc"] += omm_id.opportunity_id.user_id.login or ''
        self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, omm_id.id, force_send=False,
                                                  raise_exception=True, context=ctx)
        return omm_id


class crm_sales_target(models.Model):
    _inherit = 'crm.sales.target'

    @api.model
    def omm_expiry_mail_trigger(self):
        ctx = dict(self._context)
        current_date = datetime.date.today()
        end_date = datetime.date.today() + timedelta(days=30)
        ctx['cc'] = ''
        cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
        if cc_ids.omm_notification_ids:
            for cc_id in cc_ids.omm_notification_ids:
                if cc_id.work_email:
                    ctx["cc"] += cc_id.work_email + ','
        fields_user_ids = self.search([('id', '!=', False)])
        for omm_mismatch_id in self.env['crm.omm'].search([('id', '!=', False)]):
            count = 0
            mismatch_name = ''
            if not omm_mismatch_id.expiring_date == omm_mismatch_id.oracle_expiring_date:
                count += 1
                mismatch_name += 'Expiring Date' + ', '
            if not omm_mismatch_id.sales_stage == omm_mismatch_id.oracle_sales_stage:
                count += 1
                mismatch_name += 'Sales Stage' + ', '
            if not omm_mismatch_id.fusion_status == omm_mismatch_id.oracle_fusion_status:
                count += 1
                mismatch_name += 'Fusion Status' + ', '
            if not omm_mismatch_id.registration_status == omm_mismatch_id.oracle_registration_status:
                count += 1
                mismatch_name += 'Registration Status' + ', '
            if not omm_mismatch_id.opp_close_date == omm_mismatch_id.oracle_opp_close_date:
                count += 1
                mismatch_name += 'Opportunity Close Date' + ', '
            if count >= 1:
                omm_mismatch_id.opportunity_id.is_omm_mismatch = True
                omm_mismatch_id.write({'is_omm_mismatch': True, 'mismatch_name': mismatch_name, 'updating_check': True})
                # omm_mismatch_id.is_omm_mismatch = True
            else:
                omm_mismatch_id.opportunity_id.is_omm_mismatch = False
                omm_mismatch_id.write({'is_omm_mismatch': False, 'mismatch_name': mismatch_name, 'updating_check': True})
                # omm_mismatch_id.is_omm_mismatch = False

        for seller in fields_user_ids:
            ctx["to"] = seller.sales_target_user.user_id.login + ','

            ########## Expiring Date Mailing Function ###############

            template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                         'omm_expiring_template_one')[1]
            expiring_omm_ids = self.env['crm.omm'].search([('opportunity_id.user_id', '=', seller.sales_target_user.user_id.id),
                                                           ('expiring_date', '>=', current_date), ('expiring_date', '<=', end_date)])
            if expiring_omm_ids:
                ctx["omm_details"] = []
                list = []
                for omm_id in expiring_omm_ids:
                    list.append(str(omm_id.account_id.name))
                    list.append(str(omm_id.deal_reg_id))
                    list.append(str(omm_id.proposed_solution))
                    if omm_id.expiring_date:
                        list.append(str(omm_id.expiring_date))
                    else:
                        list.append('N/A')
                    if omm_id.oracle_expiring_date:
                        list.append(str(omm_id.oracle_expiring_date))
                    else:
                        list.append('N/A')
                ctx["omm_details"].append(list)
                self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, seller.id, force_send=False,
                                                              raise_exception=True, context=ctx)
                list[:] = []
                ctx["omm_details"][:] = []


            ############ Opportunity Close Date Mailing Function ###############

            opportunity_close_omm_ids = self.env['crm.omm'].search([('opportunity_id.user_id', '=', seller.sales_target_user.user_id.id),
                                                                    ('opp_close_date', '>=', current_date), ('opp_close_date', '<=', end_date)])
            template_opp_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                             'opportunity_close_date_template')[1]
            if opportunity_close_omm_ids:
                ctx["opp_details"] = []
                opp_date_list = []
                for omm_id in opportunity_close_omm_ids:
                    opp_date_list.append(str(omm_id.account_id.name))
                    opp_date_list.append(str(omm_id.deal_reg_id))
                    opp_date_list.append(str(omm_id.proposed_solution))
                    if omm_id.opp_close_date:
                        opp_date_list.append(str(omm_id.opp_close_date))
                    else:
                        opp_date_list.append('N/A')
                    if omm_id.oracle_opp_close_date:
                        opp_date_list.append(str(omm_id.oracle_opp_close_date))
                    else:
                        opp_date_list.append('N/A')
                ctx["opp_details"].append(opp_date_list)
                self.pool.get('email.template').send_mail(self._cr, self._uid, template_opp_id, seller.id, force_send=False,
                                                              raise_exception=True, context=ctx)
                opp_date_list[:] = []
                ctx["opp_details"][:] = []

            ########## Comparing Data Mailing Function ##############

            comparing_omm_ids = self.env['crm.omm'].search([('opportunity_id.user_id', '=', seller.sales_target_user.user_id.id)])
            template_comparing_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                             'omm_comparing_data_template')[1]
            if comparing_omm_ids:
                ctx["sales_stage_details"] = []

                for omm_id in comparing_omm_ids:
                    sales_list = []
                    result = 'N/A'
                    sales_list.append(str(omm_id.account_id.name))
                    sales_list.append(str(omm_id.deal_reg_id))
                    sales_list.append(str(omm_id.proposed_solution))
                    if omm_id.sales_stage:
                        sales_list.append(str(dict(crm_omm.AVAILABLE_SALES_STATES)[omm_id.sales_stage]))
                    else:
                        sales_list.append('N/A')
                    if omm_id.oracle_sales_stage:
                        sales_list.append(str(dict(crm_omm.AVAILABLE_SALES_STATES)[omm_id.oracle_sales_stage]))
                    else:
                        sales_list.append('N/A')
                    if omm_id.sales_stage == omm_id.oracle_sales_stage:
                        result = 'Match'
                    else:
                        result = 'Please take the require action to match the mismatch Value within 3days from receipt of this mail.'
                    sales_list.append(str(result))
                    ctx["sales_stage_details"].append(sales_list)

                ctx["expiring_date_details"] = []

                for omm_id in comparing_omm_ids:
                    expiring_list = []
                    result = 'N/A'
                    expiring_list.append(str(omm_id.account_id.name))
                    expiring_list.append(str(omm_id.deal_reg_id))
                    expiring_list.append(str(omm_id.proposed_solution))
                    if omm_id.expiring_date:
                        expiring_list.append(str(omm_id.expiring_date))
                    else:
                        expiring_list.append('N/A')
                    if omm_id.oracle_expiring_date:
                        expiring_list.append(str(omm_id.oracle_expiring_date))
                    else:
                        expiring_list.append('N/A')
                    if omm_id.expiring_date == omm_id.oracle_expiring_date:
                        result = 'Match'
                    else:
                        result = 'Please take the require action to match the mismatch Value within 3days from receipt of this mail.'
                    expiring_list.append(str(result))
                    ctx["expiring_date_details"].append(expiring_list)

                ctx["opp_close_details"] = []

                for omm_id in comparing_omm_ids:
                    opp_list = []
                    result = 'N/A'
                    opp_list.append(str(omm_id.account_id.name))
                    opp_list.append(str(omm_id.deal_reg_id))
                    opp_list.append(str(omm_id.proposed_solution))
                    if omm_id.opp_close_date:
                        opp_list.append(str(omm_id.opp_close_date))
                    else:
                        opp_list.append('N/A')
                    if omm_id.oracle_opp_close_date:
                        opp_list.append(str(omm_id.oracle_opp_close_date))
                    else:
                        opp_list.append('N/A')
                    if omm_id.opp_close_date == omm_id.oracle_opp_close_date:
                        result = 'Match'
                    else:
                        result = 'Please take the require action to match the mismatch Value within 3days from receipt of this mail.'
                    opp_list.append(str(result))
                    ctx["opp_close_details"].append(opp_list)

                ctx["registration_status_details"] = []

                for omm_id in comparing_omm_ids:
                    registration_list = []
                    result = 'N/A'
                    registration_list.append(str(omm_id.account_id.name))
                    registration_list.append(str(omm_id.deal_reg_id))
                    registration_list.append(str(omm_id.proposed_solution))
                    if omm_id.registration_status:
                        registration_list.append(str(dict(crm_omm.AVAILABLE_REGISTRATION_STATES)[omm_id.registration_status]))
                    else:
                        registration_list.append('N/A')
                    if omm_id.oracle_registration_status:
                        registration_list.append(str(dict(crm_omm.AVAILABLE_REGISTRATION_STATES)[omm_id.oracle_registration_status]))
                    else:
                        registration_list.append('N/A')
                    if omm_id.registration_status == omm_id.oracle_registration_status:
                        result = 'Match'
                    else:
                        result = 'Please take the require action to match the mismatch Value within 3days from receipt of this mail.'
                    registration_list.append(str(result))
                    ctx["registration_status_details"].append(registration_list)
                ctx["fusion_status_details"] = []
                for omm_id in comparing_omm_ids:
                    fusion_list = []
                    result = 'N/A'
                    fusion_list.append(str(omm_id.account_id.name))
                    fusion_list.append(str(omm_id.deal_reg_id))
                    fusion_list.append(str(omm_id.proposed_solution))
                    if omm_id.fusion_status:
                        fusion_list.append(str(omm_id.fusion_status))
                    else:
                        fusion_list.append('N/A')
                    if omm_id.oracle_fusion_status:
                        fusion_list.append(str(omm_id.oracle_fusion_status))
                    else:
                        fusion_list.append('N/A')
                    if omm_id.fusion_status == omm_id.oracle_fusion_status:
                        result = 'Match'
                    else:
                        result = 'Please take the require action to match the mismatch Value within 3days from receipt of this mail.'
                    fusion_list.append(str(result))
                    ctx["fusion_status_details"].append(fusion_list)
                self.pool.get('email.template').send_mail(self._cr, self._uid, template_comparing_id, seller.id, force_send=False,
                                                          raise_exception=True, context=ctx)

                sales_list[:] = []
                ctx["sales_stage_details"][:] = []

                expiring_list[:] = []
                ctx["expiring_date_details"][:] = []

                opp_list[:] = []
                ctx["opp_close_details"][:] = []

                registration_list[:] = []
                ctx["registration_status_details"][:] = []

                fusion_list[:] = []
                ctx["fusion_status_details"][:] = []


class crm_lead_omm(models.Model):
    _inherit = 'crm.lead'

    AVAILABLE_REGISTRATION_STATES = [
        ('1', 'Approved'),
        ('2', 'Extended'),
        ('3', 'Expiring'),
        ('4', 'Expired'),
        ('5', 'Declined'),
        ('6', 'Return to Partner'),
    ]

    AVAILABLE_SALES_STATES = [
        ('0', 'Assessment & Qualification'),
        ('1', 'Discovery'),
        ('2', 'Solution Development'),
        ('3', 'Solution Presentation'),
        ('4', 'Resolution'),
        ('5', 'Close'),
    ]

    AVAILABLE_STAGES = [
        ('0', 'Draft'),
        ('1', 'Approved'),
        ('2', 'OMM Submitted'),
        ('3', 'Fusion Oppty'),
        ('4', 'Rejected'),
    ]

    AVAILABLE_WIN_LOSS_REASON = [
        ('0', 'WON - Competitive Pricing'),
        ('1', 'WON - Product Fit'),
        ('2', 'WON - Relationship'),
        ('3', 'LOST - Competitor Pricing'),
        ('4', 'LOST - Competitor Product'),
        ('5', 'LOST - Competitor Relationship'),
        ('6', 'LOST - Internal Project'),
        ('7', 'LOST - Primary Reason was Serive Issue'),
        ('8', 'Closed - Alternative Oracle Solution'),
        ('9', 'Closed - Customer Not Ready / Project On Hold'),
        ('10', 'Closed - Customer Aquired'),
        ('11', 'Closed - No Business Opportunity / Poor Lead'),
    ]

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_director')
        res = super(crm_lead_omm, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                           context=context, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            if group_id not in user_group_id:
                doc = etree.XML(res['arch'])
                list1 = ['deal_reg_id', 'approved_omm_fusion', 'fusion_number', 'omm_sales_channel', 'extension_submitted',
                         'submitted_date', 'oracle_sales_stage', 'oracle_expiring_date', 'oracle_registration_status',
                         'oracle_opp_close_date', 'oracle_fusion_status', 'oracle_payment_request_status']
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('readonly', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    omm_required = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'OMM Registration')
    account_id = fields.Many2one('res.partner', 'Account Name')
    omm_id = fields.Many2one('crm.omm', 'OMM Register', readonly=True)
    oracle_product_ids = fields.Many2many('oracle.products', 'lead_oracle_product',
                                          'omm_id', 'oracle_product_id', 'Products')
    sales_team = fields.Many2one('crm.case.section', 'Sales Team')
    distributor = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Distributor (VAD)')
    distributor_company = fields.Char('Distributor Company Name')
    distributor_org = fields.Char('Org Name')
    distributor_gsi = fields.Char('GSI Account Number')
    distributor_tax = fields.Char('Tax Reg Number')
    oracle_competitor = fields.Char('Oracle Competitor')
    deal_reg_id = fields.Char('DealReg ID')
    omm_status = fields.Selection(AVAILABLE_STAGES, 'Status', default='0')
    deal_reg_type = fields.Selection([('Resale', 'Resale'), ('Referral', 'Referral')], 'DealReg Type')
    approved_omm_fusion = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Approved in OMM / Fusion')
    extension_submitted = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Extension Submitted')
    extension_close_date1 = fields.Date('Extension Close Date 1')
    extension_close_date2 = fields.Date('Extension Close Date 2')
    opp_close_date = fields.Date('Opportunity Close Date')
    oracle_opp_close_date = fields.Date('Oracle Opportunity Close Date')
    omm_date_deadline = fields.Date('Expected Closure Date')
    title = fields.Selection([('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms')], 'Title')
    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')
    omm_write_date = fields.Date('Last Update Date', readonly=True)
    omm_street = fields.Char('Street')
    omm_street2 = fields.Char('Street2')
    omm_city = fields.Char('City')
    omm_state_id = fields.Many2one('res.country.state', 'State')
    omm_zip = fields.Char('Zip', size=24)
    omm_country_id = fields.Many2one('res.country', 'Country')
    omm_region_id = fields.Many2one('res.region', 'Region')
    omm_phone = fields.Char('Phone/Mobile No.')
    omm_email = fields.Char('Company Email ID')
    proposed_solution = fields.Char('Proposed Solution')
    detailed_opportunity = fields.Char('Detailed Opportunity Description')
    solution_reason = fields.Char('Why customer needs the solution')
    department_impacted = fields.Char('Department Impacted')
    region_requirements = fields.Char('Region Specific Requirements')
    bom_price = fields.Float('Price of BOM (USD)')
    discounted_price = fields.Float('Discounted Price (USD)')
    discount = fields.Float('Discount %')
    oracle_sales_manager = fields.Char('Oracle Sales Manager (Tagged to this opportunity)')
    omm_sales_channel = fields.Selection([('direct', 'Direct'), ('indirect', 'InDirect')], 'OMM Sales Channel')
    budgets_approved = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Budgets Approved')
    direct_rfp = fields.Selection([('Direct', 'Direct'), ('RFP', 'RFP')], 'Direct /RFP')
    payment_request_status = fields.Selection([('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'),
                                               ('Rejected', 'Rejected')], 'JMR Payment Request Status')
    oracle_payment_request_status = fields.Selection([('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'),
                                                      ('Rejected', 'Rejected')], 'Oracle Payment Request Status')
    public_sector_customer = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Customer Public Sector?')
    sector_activities = fields.Many2many('public.sector.activities', 'lead_sector_activities',
                                         'omm_id', 'sector_activities_id',
                                         'Public Sector Activities ( Minimum 3 should select)')
    cloud_deal = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Cloud Deal?')
    deal_contracts = fields.Many2many('cloud.deal.contracts', 'lead_deal_contracts',
                                      'omm_id', 'deal_contracts_id', 'Cloud Deal Contracts')
    submitted_date = fields.Date('Submitted date')
    expiring_date = fields.Date('JMR Expiring date')
    oracle_expiring_date = fields.Date('Oracle Expiring date')
    registration_status = fields.Selection(AVAILABLE_REGISTRATION_STATES, 'JMR Deal Registration Status')
    oracle_registration_status = fields.Selection(AVAILABLE_REGISTRATION_STATES, 'Oracle Deal Registration Status')
    fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won'),
                                      ('Closed', 'Closed')], 'JMR Fusion Status')
    oracle_fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won'),
                                             ('Closed', 'Closed')], 'Oracle Fusion Opportunity Status')
    sales_stage = fields.Selection(AVAILABLE_SALES_STATES, 'JMR Sales Stage')
    oracle_sales_stage = fields.Selection(AVAILABLE_SALES_STATES, 'Oracle Sales Stage')
    fusion_number = fields.Char('Fusion Oppty No')
    revised_value = fields.Integer('Revised Value')
    revised_reason = fields.Char('Reason for Revised Value')
    decline_reason = fields.Char('Decline Reason')
    win_loss_reason = fields.Selection(AVAILABLE_WIN_LOSS_REASON, 'JMR Win/Loss Reason')
    oracle_win_loss_reason = fields.Selection(AVAILABLE_WIN_LOSS_REASON, 'Oracle Win/Loss Reason')
    revised_closure_date = fields.Date('Revised Closure date')
    revised_date_reason = fields.Char('Reason for Revised Closure date')
    reg_info_sales = fields.Text('Deal Registration Status Notes: Sales Support')
    reg_info_sellers = fields.Text('Deal Registration Status Notes: Seller')
    omm_notes = fields.Text('OMM Notes')
    from_omm = fields.Boolean('Is from OMM?', default=False)
    create_mail_sent = fields.Boolean('Check OMM Create Mail Sent', default=False)
    principal = fields.Selection([('Oracle', 'Oracle'), ('Temenos', 'Temenos'), ('None', 'None')], 'Principal')

    @api.one
    def write(self, vals):
        check_field = 0
        field_list = ['oracle_sales_manager', 'budgets_approved', 'omm_date_deadline', 'deal_reg_type', 'distributor',
                      'distributor_company', 'distributor_org', 'distributor_gsi', 'distributor_tax',
                      'bom_price', 'discounted_price', 'discount', 'direct_rfp', 'public_sector_customer',
                      'cloud_deal', 'sector_activities', 'deal_contracts', 'sales_stage',
                      'expiring_date', 'opp_close_date', 'payment_request_status', 'fusion_status', 'win_loss_reason',
                      'revised_value', 'revised_reason', 'decline_reason', 'revised_closure_date',
                      'revised_date_reason', 'reg_info_sales', 'reg_info_sellers', 'omm_notes']
        for field in field_list:
            if field in vals:
                check_field += 1
        ctx = dict(self._context)
        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'omm_registration_lead_updating_email_template')[1]
        ctx['action_id'] = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr', 'action_crm_omm')[1]
        lead_id = super(crm_lead_omm, self).write(vals)
        if self.omm_required == 'YES':
            if self.public_sector_customer == 'YES' and not len(self.sector_activities) >= 3:
                raise exceptions.ValidationError("Please select At least 3 Public Sector Activities")
            if self.bom_price == 0 or self.discounted_price == 0:
                raise exceptions.ValidationError("Price of BOM (USD) and Discounted Price (USD) should not be 0.0")
            self.update_omm_details()
        if not vals.get('from_omm'):
            if self.omm_id.create_mail_sent:
                if check_field > 0:
                    ctx["to"] = ''
                    to_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
                    if to_ids.omm_updates_ids:
                        for to_id in to_ids.omm_updates_ids:
                            if to_id.work_email:
                                ctx["to"] += to_id.work_email + ','
                    ctx["cc"] = ''
                    ctx["updates"] = 'Following Changes happened in above account'
                    ctx["changes"] = []

                    if vals.get('registration_status'):
                        registration_status = 'Deal Registration Status: ' + dict(self.AVAILABLE_REGISTRATION_STATES)[self.registration_status] or ''
                        ctx["changes"].append(registration_status)

                    if vals.get('sales_stage'):
                        deal_status = 'JMR Sales Stage: ' + dict(self.AVAILABLE_SALES_STATES)[self.sales_stage] or ''
                        ctx["changes"].append(deal_status)

                    if vals.get('win_loss_reason'):
                        win_loss_reason = 'Win/Loss Reason: ' + dict(self.AVAILABLE_WIN_LOSS_REASON)[self.win_loss_reason] or ''
                        ctx["changes"].append(win_loss_reason)

                    if vals.get('fusion_status'):
                        fusion_status = 'Fusion Status: ' + self.fusion_status or ''
                        ctx["changes"].append(fusion_status)

                    if vals.get('omm_sales_channel'):
                        omm_sales_channel = 'Direct /RFP: ' + self.omm_sales_channel or ''
                        ctx["changes"].append(omm_sales_channel)

                    if vals.get('payment_request_status'):
                        payment_request_status = 'OMM Payment Request Status: ' + self.payment_request_status or ''
                        ctx["changes"].append(payment_request_status)

                    if vals.get('opp_close_date'):
                        opp_close_date = 'Opportunity Close Date: ' + str(self.opp_close_date or '')
                        ctx["changes"].append(opp_close_date)

                    if vals.get('omm_date_deadline'):
                        omm_date_deadline = 'Expected Closure Date: ' + str(self.omm_date_deadline or '')
                        ctx["changes"].append(omm_date_deadline)

                    if vals.get('expiring_date'):
                        expiring_date = 'Expiring date: ' + str(self.expiring_date or '')
                        ctx["changes"].append(expiring_date)

                    if vals.get('bom_price'):
                        bom_price = 'Price of BOM (USD): ' + str(self.bom_price or '')
                        ctx["changes"].append(bom_price)

                    if vals.get('distributor'):
                        distributor = 'Distributor (VAD): ' + str(self.distributor or '')
                        ctx["changes"].append(distributor)

                    if vals.get('distributor_company'):
                        distributor_company = 'Distributor Company Name: ' + str(self.distributor_company or '')
                        ctx["changes"].append(distributor_company)

                    if vals.get('distributor_org'):
                        distributor_org = 'Distributor Org Name: ' + str(self.distributor_org or '')
                        ctx["changes"].append(distributor_org)

                    if vals.get('distributor_gsi'):
                        distributor_gsi = 'GSI Account Number: ' + str(self.distributor_gsi or '')
                        ctx["changes"].append(distributor_gsi)

                    if vals.get('distributor_tax'):
                        distributor_tax = 'Tax Reg Number: ' + str(self.distributor_tax or '')
                        ctx["changes"].append(distributor_tax)

                    if vals.get('discounted_price'):
                        discounted_price = 'Discounted Price (USD): ' + str(self.discounted_price or '')
                        ctx["changes"].append(discounted_price)

                    if vals.get('discount'):
                        discount = 'Discount %: ' + str(self.discount or '')
                        ctx["changes"].append(discount)

                    if vals.get('deal_reg_type'):
                        deal_reg_type = 'DealReg Type: ' + str(self.deal_reg_type or '')
                        ctx["changes"].append(deal_reg_type)

                    if vals.get('budgets_approved'):
                        budgets_approved = 'Budgets Approved: ' + str(self.budgets_approved or '')
                        ctx["changes"].append(budgets_approved)

                    if vals.get('direct_rfp'):
                        direct_rfp = 'Direct /RFP: ' + str(self.direct_rfp or '')
                        ctx["changes"].append(direct_rfp)

                    if vals.get('extension_submitted'):
                        extension_submitted = 'Extension Submitted: ' + str(self.extension_submitted or '')
                        ctx["changes"].append(extension_submitted)

                    if vals.get('extension_close_date1'):
                        extension_close_date1 = 'Extension Close Date 1: ' + str(self.extension_close_date1 or '')
                        ctx["changes"].append(extension_close_date1)

                    if vals.get('extension_close_date2'):
                        extension_close_date2 = 'Extension Close Date 2: ' + str(self.extension_close_date2 or '')
                        ctx["changes"].append(extension_close_date2)

                    if vals.get('submitted_date'):
                        submitted_date = 'Submitted Date: ' + str(self.submitted_date or '')
                        ctx["changes"].append(submitted_date)

                    if vals.get('decline_reason'):
                        decline_reason = 'Decline Reason: ' + str(self.decline_reason or '')
                        ctx["changes"].append(decline_reason)

                    if vals.get('oracle_sales_manager'):
                        oracle_sales_manager = 'Oracle Sales Manager (Tagged to this opportunity): ' + str(self.oracle_sales_manager or '')
                        ctx["changes"].append(oracle_sales_manager)

                    if vals.get('revised_value'):
                        revised_value = 'Revised Value: ' + str(self.revised_value or '')
                        ctx["changes"].append(revised_value)

                    if vals.get('revised_reason'):
                        revised_reason = 'Reason for Revised Value: ' + str(self.revised_reason or '')
                        ctx["changes"].append(revised_reason)

                    if vals.get('revised_closure_date'):
                        revised_closure_date = 'Revised Closure Date: ' + str(self.revised_closure_date or '')
                        ctx["changes"].append(revised_closure_date)

                    if vals.get('revised_date_reason'):
                        revised_date_reason = 'Reason for Revised Closure Date: ' + str(self.revised_date_reason or '')
                        ctx["changes"].append(revised_date_reason)

                    if vals.get('reg_info_sellers'):
                        reg_info_sellers = 'Deal Registration Status Notes: Seller: ' + str(self.reg_info_sellers or '')
                        ctx["changes"].append(reg_info_sellers)

                    if vals.get('reg_info_sales'):
                        reg_info_sales = 'Deal Registration Status Notes: Sales Support: ' + str(self.reg_info_sales or '')
                        ctx["changes"].append(reg_info_sales)

                    if vals.get('omm_notes'):
                        omm_notes = 'OMM Notes: ' + str(self.omm_notes or '')
                        ctx["changes"].append(omm_notes)

                    cc_ids = self.env['hr.department.responsible'].search([('id', '=', 1)])
                    if cc_ids.omm_notification_ids:
                        for cc_id in cc_ids.omm_notification_ids:
                            if cc_id.work_email:
                                ctx["cc"] += cc_id.work_email + ','
                    if self.user_id:
                        ctx["cc"] += self.user_id.login + ','
                    self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, self.id, force_send=False,
                                                              raise_exception=True, context=ctx)
        return lead_id

    @api.onchange('principal', 'deal')
    def onchange_omm_deal(self):
        if self.principal == 'Oracle' and self.deal in ['License', 'License & Service']:
            self.omm_required = 'YES'
        else:
            self.omm_required = 'NO'

    @api.one
    def update_omm_details(self):
        ommObj = self.env['crm.omm']
        oracle_product_ids = []
        if self.oracle_product_ids:
            for oracle_products_id in self.oracle_product_ids:
                oracle_product_ids.append(oracle_products_id.id)
        sector_activities_list = []
        if self.sector_activities:
            for sector_activities_id in self.sector_activities:
                sector_activities_list.append(sector_activities_id.id)
        deal_contracts_list = []
        if self.deal_contracts:
            for deal_contracts_id in self.deal_contracts:
                deal_contracts_list.append(deal_contracts_id.id)
        omm_id = ommObj.search([('opportunity_id', '=', self.id)])
        if not omm_id:
            omm_id = ommObj.create({
                'account_id': self.account_id.id,
                'opportunity_id': self.id,
                'oracle_product_ids': [(6, 0, oracle_product_ids)],
                'sales_team': self.sales_team.id,
                'oracle_competitor': self.oracle_competitor,
                'deal_reg_id': self.deal_reg_id,
                'deal_reg_type': self.deal_reg_type,
                'approved_omm_fusion': self.approved_omm_fusion,
                'extension_submitted': self.extension_submitted,
                'extension_close_date1': self.extension_close_date1,
                'extension_close_date2': self.extension_close_date2,
                'write_date': self.omm_write_date,
                'opp_close_date': self.opp_close_date,
                'date_deadline': self.omm_date_deadline,
                'title': self.title,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'street': self.omm_street,
                'street2': self.omm_street2,
                'city': self.omm_city,
                'state_id': self.omm_state_id.id,
                'zip': self.omm_zip,
                'country_id': self.omm_country_id.id,
                'region_id': self.omm_region_id.id,
                'phone': self.omm_phone,
                'email': self.omm_email,
                'proposed_solution': self.proposed_solution,
                'detailed_opportunity': self.detailed_opportunity,
                'solution_reason': self.solution_reason,
                'department_impacted': self.department_impacted,
                'region_requirements': self.region_requirements,
                'bom_price': self.bom_price,
                'discounted_price': self.discounted_price,
                'discount': self.discount,
                'oracle_sales_manager': self.oracle_sales_manager,
                'omm_sales_channel': self.omm_sales_channel,
                'budgets_approved': self.budgets_approved,
                'direct_rfp': self.direct_rfp,
                'payment_request_status': self.payment_request_status,
                'public_sector_customer': self.public_sector_customer,
                'sector_activities': [(6, 0, sector_activities_list)],
                'cloud_deal': self.cloud_deal,
                'deal_contracts': [(6, 0, deal_contracts_list)],
                'submitted_date': self.submitted_date,
                'expiring_date': self.expiring_date,
                'registration_status': self.registration_status,
                'fusion_status': self.fusion_status,
                'fusion_number': self.fusion_number,
                'sales_stage': self.sales_stage,
                'revised_value': self.revised_value,
                'revised_reason': self.revised_reason,
                'decline_reason': self.decline_reason,
                'win_loss_reason': self.win_loss_reason,
                'revised_closure_date': self.revised_closure_date,
                'revised_date_reason': self.revised_date_reason,
                'reg_info_sales': self.reg_info_sales,
                'reg_info_sellers': self.reg_info_sellers,
                'omm_notes': self.omm_notes,
                'distributor': self.distributor,
                'distributor_company': self.distributor_company,
                'distributor_org': self.distributor_org,
                'distributor_gsi': self.distributor_gsi,
                'distributor_tax': self.distributor_tax,
            })
            self.omm_id = omm_id[0].id
        else:
            if self.omm_id:
                vals = {
                    'account_id': self.account_id.id,
                    'opportunity_id': self.id,
                    'oracle_product_ids': [(6, 0, oracle_product_ids)],
                    'sales_team': self.sales_team.id,
                    'oracle_competitor': self.oracle_competitor,
                    'deal_reg_id': self.deal_reg_id,
                    'deal_reg_type': self.deal_reg_type,
                    'approved_omm_fusion': self.approved_omm_fusion,
                    'extension_submitted': self.extension_submitted,
                    'extension_close_date1': self.extension_close_date1,
                    'extension_close_date2': self.extension_close_date2,
                    'write_date': self.omm_write_date,
                    'opp_close_date': self.opp_close_date,
                    'date_deadline': self.omm_date_deadline,
                    # 'title': self.title,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'street': self.omm_street,
                    'street2': self.omm_street2,
                    'city': self.omm_city,
                    'state_id': self.omm_state_id.id,
                    'zip': self.omm_zip,
                    'country_id': self.omm_country_id.id,
                    'region_id': self.omm_region_id.id,
                    'phone': self.omm_phone,
                    'email': self.omm_email,
                    'proposed_solution': self.proposed_solution,
                    'detailed_opportunity': self.detailed_opportunity,
                    'solution_reason': self.solution_reason,
                    'department_impacted': self.department_impacted,
                    'region_requirements': self.region_requirements,
                    'bom_price': self.bom_price,
                    'discounted_price': self.discounted_price,
                    'discount': self.discount,
                    'oracle_sales_manager': self.oracle_sales_manager,
                    'omm_sales_channel': self.omm_sales_channel,
                    'budgets_approved': self.budgets_approved,
                    'direct_rfp': self.direct_rfp,
                    'payment_request_status': self.payment_request_status,
                    'public_sector_customer': self.public_sector_customer,
                    'sector_activities': [(6, 0, sector_activities_list)],
                    'cloud_deal': self.cloud_deal,
                    'deal_contracts': [(6, 0, deal_contracts_list)],
                    'submitted_date': self.submitted_date,
                    'expiring_date': self.expiring_date,
                    'registration_status': self.registration_status,
                    'fusion_status': self.fusion_status,
                    'fusion_number': self.fusion_number,
                    'sales_stage': self.sales_stage,
                    'revised_value': self.revised_value,
                    'revised_reason': self.revised_reason,
                    'decline_reason': self.decline_reason,
                    'win_loss_reason': self.win_loss_reason,
                    'revised_closure_date': self.revised_closure_date,
                    'revised_date_reason': self.revised_date_reason,
                    'reg_info_sales': self.reg_info_sales,
                    'reg_info_sellers': self.reg_info_sellers,
                    'omm_notes': self.omm_notes,
                    'from_lead': True,
                    'updating_check': True,
                }
                omm_id.write(vals)
        return True


class omm_mismatch_sales_stage(models.Model):
    _name = 'omm.mismatch.sales.stage'
    _description = 'OMM Mismatch (Sales Stage)'
    _order = "id desc"
    _rec_name = "omm_id"

    omm_id = fields.Many2one('crm.omm', 'OMM Reference', readonly=True)
    account_id = fields.Many2one('res.partner', 'Account Name', related="omm_id.account_id", store=True, readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Lead/Opportunity Name', related="omm_id.opportunity_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="omm_id.department_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Seller', related="opportunity_id.user_id", store=True, readonly=True)
    proposed_solution = fields.Char('Proposed Solution', related="omm_id.proposed_solution", store=True, readonly=True)
    deal_reg_id = fields.Char('Deal Reg ID', related="omm_id.deal_reg_id", store=True, readonly=True)
    sales_stage = fields.Selection(crm_omm.AVAILABLE_SALES_STATES, 'JMR Sales Stage', related="omm_id.sales_stage",
                                   store=True, readonly=True)
    oracle_sales_stage = fields.Selection(crm_omm.AVAILABLE_SALES_STATES, 'Oracle Sales Stage',
                                          related="omm_id.oracle_sales_stage", store=True, readonly=True)


class omm_mismatch_expiring_date(models.Model):
    _name = 'omm.mismatch.expiring.date'
    _description = 'OMM Mismatch (Expiring Date)'
    _order = "id desc"
    _rec_name = "omm_id"

    omm_id = fields.Many2one('crm.omm', 'OMM Reference', readonly=True)
    account_id = fields.Many2one('res.partner', 'Account Name', related="omm_id.account_id", store=True, readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Lead/Opportunity Name', related="omm_id.opportunity_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="omm_id.department_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Seller', related="omm_id.user_id", store=True, readonly=True)
    proposed_solution = fields.Char('Proposed Solution', related="omm_id.proposed_solution", store=True, readonly=True)
    deal_reg_id = fields.Char('Deal Reg ID', related="omm_id.deal_reg_id", store=True, readonly=True)
    expiring_date = fields.Date('JMR Expiring date', related="omm_id.expiring_date", store=True, readonly=True)
    oracle_expiring_date = fields.Date('Oracle Expiring date', related="omm_id.oracle_expiring_date", store=True, readonly=True)


class omm_mismatch_opportunity_date(models.Model):
    _name = 'omm.mismatch.opportunity.date'
    _description = 'OMM Mismatch (Opportunity Close Date)'
    _order = "id desc"
    _rec_name = "omm_id"

    omm_id = fields.Many2one('crm.omm', 'OMM Reference', readonly=True)
    account_id = fields.Many2one('res.partner', 'Account Name', related="omm_id.account_id", store=True, readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Lead/Opportunity Name', related="omm_id.opportunity_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="omm_id.department_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Seller', related="omm_id.user_id", store=True, readonly=True)
    proposed_solution = fields.Char('Proposed Solution', related="omm_id.proposed_solution", store=True, readonly=True)
    deal_reg_id = fields.Char('Deal Reg ID', related="omm_id.deal_reg_id", store=True, readonly=True)
    opp_close_date = fields.Date('Opportunity Close Date', related="omm_id.opp_close_date", store=True, readonly=True)
    oracle_opp_close_date = fields.Date('Oracle Opportunity Close Date', related="omm_id.oracle_opp_close_date",
                                        store=True, readonly=True)

class omm_mismatch_fusion_status(models.Model):
    _name = 'omm.mismatch.fusion.status'
    _description = 'OMM Mismatch (Fusion Opportunity Status)'
    _order = "id desc"
    _rec_name = "omm_id"

    omm_id = fields.Many2one('crm.omm', 'OMM Reference', readonly=True)
    account_id = fields.Many2one('res.partner', 'Account Name', related="omm_id.account_id", store=True, readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Lead/Opportunity Name', related="omm_id.opportunity_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="omm_id.department_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Seller', related="omm_id.user_id", store=True, readonly=True)
    proposed_solution = fields.Char('Proposed Solution', related="omm_id.proposed_solution", store=True, readonly=True)
    deal_reg_id = fields.Char('Deal Reg ID', related="omm_id.deal_reg_id", store=True, readonly=True)
    fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won'),
                                      ('Closed', 'Closed')],
                                     'Fusion Status', related="omm_id.fusion_status", store=True, readonly=True)
    oracle_fusion_status = fields.Selection([('Open', 'Open'), ('Closed and Lost', 'Closed and Lost'), ('Closed and Won', 'Closed and Won')],
                                            'Oracle Fusion Opportunity Status', related="omm_id.oracle_fusion_status", store=True, readonly=True)

