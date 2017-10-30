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
import datetime
from datetime import timedelta


class opportunity_line(models.Model):
    _name = 'opportunity.line'
    _description = 'Opportunity Line'
    _order = "id desc"

    AVAILABLE_STAGES = [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'Aug'),
        ('9', 'Sept'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),
    ]

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    lead_id = fields.Many2one('crm.lead', 'Opportunity Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', related="lead_id.partner_id", store=True, readonly=True)
    date_deadline = fields.Date('Expected Closing', related="lead_id.date_deadline", store=True, readonly=True)
    date_converted = fields.Date('Opportunity Converted Date', related="lead_id.date_converted", store=True, readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage', related="lead_id.stage_id", store=True, readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="lead_id.country_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'seller_quarter_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('seller.opportunity.pipeline.build', 'Reference', readonly=True)

    title_action = fields.Char('Title Action', related="lead_id.title_action", store=True, readonly=True)
    is_omm_mismatch = fields.Boolean('OMM Mismatch', related="lead_id.is_omm_mismatch", store=True, readonly=True)
    date_action = fields.Date('Date Action', related="lead_id.date_action", store=True, readonly=True)
    omm_id = fields.Many2one('crm.omm', 'OMM Register', related="lead_id.omm_id", store=True, readonly=True)
    seller_call_deal = fields.Selection(AVAILABLE_STAGES, 'Seller Call Deal Month', related="lead_id.seller_call_deal",
                                        store=True, readonly=True)
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Seller Call Deal Quarter',
                                         related="lead_id.call_deal_quarter", store=True, readonly=True)
    bu_call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'BU Call Deal Quarter',
                                            related="lead_id.bu_call_deal_quarter", store=True, readonly=True)
    bu_call_deal = fields.Selection(AVAILABLE_STAGES, 'BU Call Deal Month', related="lead_id.bu_call_deal", store=True,
                                    readonly=True)


class lead_line(models.Model):
    _name = 'lead.line'
    _description = 'Lead Line'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', related="lead_id.partner_id", store=True, readonly=True)
    date_deadline = fields.Date('Expected Closing', related="lead_id.date_deadline", store=True, readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage', related="lead_id.stage_id", store=True, readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="lead_id.country_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'seller_quarter_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('seller.opportunity.pipeline.build', 'Reference', readonly=True)

    is_omm_mismatch = fields.Boolean('OMM Mismatch', related="lead_id.is_omm_mismatch", store=True, readonly=True)
    omm_id = fields.Many2one('crm.omm', 'OMM Register', related="lead_id.omm_id", store=True, readonly=True)


class seller_bu_opportunity_pipeline_build(models.Model):
    _name = 'seller.bu.opportunity.pipeline.build'
    _description = 'Seller BU Opportunity Pipeline Build'
    _rec_name = 'name'
    _order = 'name'

    @api.one
    @api.depends('pipeline_build_value', 'opportunity_value')
    def _pipeline_build_achievement(self):
        if self.pipeline_build_value and self.opportunity_value:
            self.pipeline_build_achievement = (self.opportunity_value * 100 / self.pipeline_build_value)

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    name = fields.Char('Quarter', readonly=True)
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Pipeline Build Achievement', readonly=True)
    lead_count = fields.Integer('Lead Count', readonly=True)
    pipeline_build_value = fields.Float('Pipeline Build Target', readonly=False)
    pipeline_build_achievement = fields.Float('Pipeline Build Achievement', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    ref_id = fields.Many2one('seller.opportunity.pipeline.build', 'Reference', readonly=True)
    color = fields.Integer('Colour', default=6)

class seller_opportunity_pipeline_build(models.Model):
    _name = 'seller.opportunity.pipeline.build'
    _description = 'Seller Opportunity Pipeline Build'
    _rec_name = 'sales_target_user'
    # _order = 'name'

    @api.one
    @api.depends('pipeline_build_value', 'opportunity_value')
    def _pipeline_build_achievement(self):
        if self.pipeline_build_value and self.opportunity_value:
            self.pipeline_build_achievement = (self.opportunity_value * 100 / self.pipeline_build_value)
        self.pipeline_build_variant = float(self.opportunity_value) - float(self.pipeline_build_value)

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    # name = fields.Char('Quarter', readonly=True)
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Pipeline Build Achievement', readonly=True)
    lead_count = fields.Integer('Lead Count', readonly=True)
    pipeline_build_value = fields.Float('Pipeline Build Target', readonly=False)
    pipeline_build_variant = fields.Float('Pipeline Build Variant', compute=_pipeline_build_achievement, store=True,
                                          readonly=True)
    pipeline_build_achievement = fields.Float('Pipeline Build Achievement %', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    seller_bu_pipeline_build_line = fields.One2many('seller.bu.opportunity.pipeline.build', 'ref_id',
                                                    'Seller BU Opportunity Pipeline build', readonly=False)
    ref_id = fields.Many2one('opportunity.pipeline.build', 'Reference', readonly=True)
    opportunity_line = fields.One2many('opportunity.line', 'ref_id', 'Opportunity Line', readonly=True)
    lead_line = fields.One2many('lead.line', 'ref_id', 'Lead Line', readonly=True)
    color = fields.Integer('Colour', default=6)


class opportunity_pipeline_build(models.Model):
    _name = 'opportunity.pipeline.build'
    _description = 'Opportunity Pipeline Build'
    _rec_name = 'name'
    _order = 'name'

    @api.one
    @api.depends('pipeline_build_value', 'opportunity_value')
    def _pipeline_build_achievement(self):
        if self.pipeline_build_value and self.opportunity_value:
            self.pipeline_build_achievement = (self.opportunity_value * 100 / self.pipeline_build_value)
        self.pipeline_build_variant = float(self.opportunity_value) - float(self.pipeline_build_value)

    name = fields.Char('Quarter', readonly=True)
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Pipeline Build Achievement', readonly=True)
    lead_count = fields.Integer('Lead Count', readonly=True)
    pipeline_build_value = fields.Float('Pipeline Build Target', readonly=False)
    pipeline_build_variant = fields.Float('Pipeline Build Variant', compute=_pipeline_build_achievement, store=True,
                                          readonly=True)
    pipeline_build_achievement = fields.Float('Pipeline Build Achievement %', compute='_pipeline_build_achievement',
                                              store=True, readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year', readonly=True)
    seller_pipeline_build_line = fields.One2many('seller.opportunity.pipeline.build', 'ref_id',
                                                 'Seller Opportunity Pipeline build', readonly=False)
    color = fields.Integer('Colour', default=6)

    @api.model
    def run_opportunity_pipeline_build(self):
        crmLeadObj = self.env['crm.lead']
        case_stageObj = self.env['crm.case.stage']
        seller_oppObj = self.env['seller.opportunity.pipeline.build']
        seller_bu_oppObj = self.env['seller.bu.opportunity.pipeline.build']
        oppoertunity_Obj = self.env['opportunity.line']
        lead_Obj = self.env['lead.line']
        seller_bu_oppObj = self.env['seller.bu.opportunity.pipeline.build']
        current_date = datetime.date.today()
        opp_stage_list = []
        opp_stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])
        if opp_stage_ids:
            for stage in opp_stage_ids:
                opp_stage_list.append(stage.id)
        lead_stages_list = []
        lead_stages_ids = case_stageObj.search([('type', '=', 'lead')])
        if lead_stages_ids:
            for stage in lead_stages_ids:
                lead_stages_list.append(stage.id)
        fiscalyear_id = None
        fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                ('date_stop', '>=', current_date)])
        q1_pipe_value = 0.0
        q2_pipe_value = 0.0
        q3_pipe_value = 0.0
        q4_pipe_value = 0.0
        q1_opp_count = []
        q2_opp_count = []
        q3_opp_count = []
        q4_opp_count = []
        q1_lead_count = []
        q2_lead_count = []
        q3_lead_count = []
        q4_lead_count = []
        if fiscalyear_ids:
            fiscalyear_id = fiscalyear_ids[0]
        if fiscalyear_id:
            saleperson_target_ids = self.env['saleperson.target'].search([('manager_user_relation_id', '!=', False)])
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

            ## Ovaral Quarter wise ##

            ### Lead Browsing ###
            for lead_id in crmLeadObj.search([('create_date', '>=', q1_start_date),
                                              ('create_date', '<=', q1_end_date),
                                              ('stage_id', 'in', lead_stages_list)]):
                q1_lead_count.append(lead_id.id)
            for lead_id in crmLeadObj.search([('create_date', '>=', q2_start_date),
                                              ('create_date', '<=', q2_end_date),
                                              ('stage_id', 'in', lead_stages_list)]):
                q2_lead_count.append(lead_id.id)
            for lead_id in crmLeadObj.search([('create_date', '>=', q3_start_date),
                                              ('create_date', '<=', q3_end_date),
                                              ('stage_id', 'in', lead_stages_list)]):
                q3_lead_count.append(lead_id.id)
            for lead_id in crmLeadObj.search([('create_date', '>=', q4_start_date),
                                              ('create_date', '<=', q4_end_date),
                                              ('stage_id', 'in', lead_stages_list)]):
                q4_lead_count.append(lead_id.id)

            ### Opportunity Browsing ###
            for opportunity_id in crmLeadObj.search([('date_converted', '>=', q1_start_date),
                                                     ('date_converted', '<=', q1_end_date),
                                                     ('stage_id', 'in', opp_stage_list)]):
                q1_pipe_value += opportunity_id.planned_revenue
                q1_opp_count.append(opportunity_id.id)


            for opportunity_id in crmLeadObj.search([('date_converted', '>=', q2_start_date),
                                                     ('date_converted', '<=', q2_end_date),
                                                     ('stage_id', 'in', opp_stage_list)]):
                q2_pipe_value += opportunity_id.planned_revenue
                q2_opp_count.append(opportunity_id.id)
            for opportunity_id in crmLeadObj.search([('date_converted', '>=', q3_start_date),
                                                     ('date_converted', '<=', q3_end_date),
                                                     ('stage_id', 'in', opp_stage_list)]):
                q3_pipe_value += opportunity_id.planned_revenue
                q3_opp_count.append(opportunity_id.id)
            for opportunity_id in crmLeadObj.search([('date_converted', '>=', q4_start_date),
                                                     ('date_converted', '<=', q4_end_date),
                                                     ('stage_id', 'in', opp_stage_list)]):
                q4_pipe_value += opportunity_id.planned_revenue
                q3_opp_count.append(opportunity_id.id)

            q1_pipeline_build_id = self.search([('fiscalyear_id', '=', fiscalyear_id.id), ('name', '=', 'Q1 (AMJ)')])
            if len(q1_pipeline_build_id) > 1:
                q1_pipeline_build_id = q1_pipeline_build_id[0]
            if not q1_pipeline_build_id:
                q1_pipeline_build_id = self.create({'name': 'Q1 (AMJ)',
                                                    'fiscalyear_id': fiscalyear_id.id,
                                                    'opportunity_count': len(q1_opp_count),
                                                    'opportunity_value': q1_pipe_value,
                                                    'lead_count': len(q1_lead_count),
                                                    })
            else:
                q1_pipeline_build_id.opportunity_value = q1_pipe_value
                q1_pipeline_build_id.opportunity_count = len(q1_opp_count)
                q1_pipeline_build_id.lead_count = len(q1_lead_count)

            q2_pipeline_build_id = self.search([('fiscalyear_id', '=', fiscalyear_id.id), ('name', '=', 'Q2 (JAS)')])
            if len(q2_pipeline_build_id) > 1:
                q2_pipeline_build_id = q2_pipeline_build_id[0]
            if not q2_pipeline_build_id:
                q2_pipeline_build_id = self.create({'name': 'Q2 (JAS)',
                                                     'fiscalyear_id': fiscalyear_id.id,
                                                     'opportunity_count': len(q2_opp_count),
                                                     'opportunity_value': q2_pipe_value,
                                                     'lead_count': len(q2_lead_count),
                                                    })
            else:
                q2_pipeline_build_id.opportunity_value = q2_pipe_value
                q2_pipeline_build_id.opportunity_count = len(q2_opp_count)
                q2_pipeline_build_id.lead_count = len(q2_lead_count)

            q3_pipeline_build_id = self.search([('fiscalyear_id', '=', fiscalyear_id.id), ('name', '=', 'Q3 (OND)')])
            if len(q3_pipeline_build_id) > 1:
                q3_pipeline_build_id = q3_pipeline_build_id[0]
            if not q3_pipeline_build_id:
                q3_pipeline_build_id = self.create({'name': 'Q3 (OND)',
                                                     'fiscalyear_id': fiscalyear_id.id,
                                                     'opportunity_count': len(q3_opp_count),
                                                     'opportunity_value': q3_pipe_value,
                                                     'lead_count': len(q3_lead_count),
                                                    })
            else:
                q3_pipeline_build_id.opportunity_value = q3_pipe_value
                q3_pipeline_build_id.opportunity_count = len(q3_opp_count)
                q3_pipeline_build_id.lead_count = len(q3_lead_count)

            q4_pipeline_build_id = self.search([('fiscalyear_id', '=', fiscalyear_id.id), ('name', '=', 'Q4 (JFM)')])
            if len(q4_pipeline_build_id) > 1:
                q4_pipeline_build_id = q4_pipeline_build_id[0]
            if not q4_pipeline_build_id:
                q4_pipeline_build_id = self.create({'name': 'Q4 (JFM)',
                                                     'fiscalyear_id': fiscalyear_id.id,
                                                     'opportunity_count': len(q4_opp_count),
                                                     'opportunity_value': q4_pipe_value,
                                                     'lead_count': len(q4_lead_count),
                                                    })
            else:
                q4_pipeline_build_id.opportunity_value = q4_pipe_value
                q4_pipeline_build_id.opportunity_count = len(q4_opp_count)
                q4_pipeline_build_id.lead_count = len(q4_lead_count)

            ## Seller Quarter wise ##

            for fields_user in saleperson_target_ids:
                seller_total_pipe_value = 0.0
                seller_total_opp_count = []
                seller_total_lead_count = []
                seller_q1_pipe_value = 0.0
                seller_q2_pipe_value = 0.0
                seller_q3_pipe_value = 0.0
                seller_q4_pipe_value = 0.0
                seller_q1_opp_count = []
                seller_q2_opp_count = []
                seller_q3_opp_count = []
                seller_q4_opp_count = []
                seller_q1_lead_count = []
                seller_q2_lead_count = []
                seller_q3_lead_count = []
                seller_q4_lead_count = []
                for lead_id in crmLeadObj.search([('create_date', '>=', q1_start_date),
                                                  ('create_date', '<=', q1_end_date),
                                                  ('user_id', '=', fields_user.user_id.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    seller_q1_lead_count.append(lead_id.id)
                    seller_total_lead_count.append(lead_id.id)
                for lead_id in crmLeadObj.search([('create_date', '>=', q2_start_date),
                                                  ('create_date', '<=', q2_end_date),
                                                  ('user_id', '=', fields_user.user_id.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    seller_q2_lead_count.append(lead_id.id)
                    seller_total_lead_count.append(lead_id.id)
                for lead_id in crmLeadObj.search([('create_date', '>=', q3_start_date),
                                                  ('create_date', '<=', q3_end_date),
                                                  ('user_id', '=', fields_user.user_id.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    seller_q3_lead_count.append(lead_id.id)
                    seller_total_lead_count.append(lead_id.id)
                for lead_id in crmLeadObj.search([('create_date', '>=', q4_start_date),
                                                  ('create_date', '<=', q4_end_date),
                                                  ('user_id', '=', fields_user.user_id.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    seller_q4_lead_count.append(lead_id.id)
                    seller_total_lead_count.append(lead_id.id)

                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q1_start_date),
                                                         ('date_converted', '<=', q1_end_date),
                                                         ('user_id', '=', fields_user.user_id.id),
                                                         ('stage_id', 'in', opp_stage_list)]):
                    seller_q1_pipe_value += opportunity_id.planned_revenue
                    seller_q1_opp_count.append(opportunity_id.id)
                    seller_total_pipe_value += opportunity_id.planned_revenue
                    seller_total_opp_count.append(opportunity_id.id)
                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q2_start_date),
                                                         ('date_converted', '<=', q2_end_date),
                                                         ('user_id', '=', fields_user.user_id.id),
                                                         ('stage_id', 'in', opp_stage_list)]):
                    seller_q2_pipe_value += opportunity_id.planned_revenue
                    seller_q2_opp_count.append(opportunity_id.id)
                    seller_total_pipe_value += opportunity_id.planned_revenue
                    seller_total_opp_count.append(opportunity_id.id)
                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q3_start_date),
                                                         ('date_converted', '<=', q3_end_date),
                                                         ('user_id', '=', fields_user.user_id.id),
                                                         ('stage_id', 'in', opp_stage_list)]):
                    seller_q3_pipe_value += opportunity_id.planned_revenue
                    seller_q3_opp_count.append(opportunity_id.id)
                    seller_total_pipe_value += opportunity_id.planned_revenue
                    seller_total_opp_count.append(opportunity_id.id)
                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q4_start_date),
                                                         ('date_converted', '<=', q4_end_date),
                                                         ('user_id', '=', fields_user.user_id.id),
                                                         ('stage_id', 'in', opp_stage_list)]):
                    seller_q4_pipe_value += opportunity_id.planned_revenue
                    seller_q4_opp_count.append(opportunity_id.id)
                    seller_total_pipe_value += opportunity_id.planned_revenue
                    seller_total_opp_count.append(opportunity_id.id)

                q1_seller_id = seller_oppObj.search([('ref_id', '=', q1_pipeline_build_id.id),
                                                     ('fiscalyear_id', '=', fiscalyear_id.id),
                                                     ('sales_target_user', '=', fields_user.id)])
                if len(q1_seller_id) > 1:
                    q1_seller_id = q1_seller_id[0]
                if not q1_seller_id:
                    q1_seller_id = seller_oppObj.create({'sales_target_user': fields_user.id,
                                                         'fiscalyear_id': fiscalyear_id.id,
                                                         'opportunity_count': len(seller_q1_opp_count),
                                                         'opportunity_value': seller_q1_pipe_value,
                                                         'lead_count': len(seller_q1_lead_count),
                                                         'ref_id': q1_pipeline_build_id.id})
                else:
                    q1_seller_id.opportunity_count = len(seller_q1_opp_count)
                    q1_seller_id.opportunity_value = seller_q1_pipe_value
                    q1_seller_id.lead_count = len(seller_q1_lead_count)

                if q1_seller_id.sales_target_user.manager_user_relation_id.user_id:
                    q1_seller_id.sales_manager = q1_seller_id.sales_target_user.manager_user_relation_id.user_id.id

                for opp_id in seller_q1_opp_count:
                    q1_opp_id = oppoertunity_Obj.search([('ref_id', '=', q1_seller_id.id),
                                                        ('lead_id', '=', opp_id)])
                    if len(q1_opp_id) > 1:
                        q1_opp_id = q1_opp_id[0]
                    if not q1_opp_id:
                        oppoertunity_Obj.create({'lead_id': opp_id,
                                                 'ref_id': q1_seller_id.id,
                                                 })
                # lead Line Creation #
                for lead_id in seller_q1_lead_count:
                    q1_lead_id = lead_Obj.search([('ref_id', '=', q1_seller_id.id),
                                                      ('lead_id', '=', lead_id)])
                    if len(q1_lead_id) > 1:
                        q1_lead_id = q1_lead_id[0]
                    if not q1_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q1_seller_id.id,
                                         })

                q2_seller_id = seller_oppObj.search([('ref_id', '=', q2_pipeline_build_id.id),
                                                     ('fiscalyear_id', '=', fiscalyear_id.id),
                                                     ('sales_target_user', '=', fields_user.id)])
                if len(q2_seller_id) > 1:
                    q2_seller_id = q2_seller_id[0]
                if not q2_seller_id:
                    q2_seller_id = seller_oppObj.create({'sales_target_user': fields_user.id,
                                                         'fiscalyear_id': fiscalyear_id.id,
                                                         'opportunity_count': len(seller_q2_opp_count),
                                                         'opportunity_value': seller_q2_pipe_value,
                                                         'lead_count': len(seller_q2_lead_count),
                                                         'ref_id': q2_pipeline_build_id.id})
                else:
                    q2_seller_id.opportunity_count = len(seller_q2_opp_count)
                    q2_seller_id.opportunity_value = seller_q2_pipe_value
                    q2_seller_id.lead_count = len(seller_q2_lead_count)

                if q2_seller_id.sales_target_user.manager_user_relation_id.user_id:
                    q2_seller_id.sales_manager = q2_seller_id.sales_target_user.manager_user_relation_id.user_id.id

                for opp_id in seller_q2_opp_count:
                    q2_opp_id = oppoertunity_Obj.search([('ref_id', '=', q2_seller_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q2_opp_id) > 1:
                        q2_opp_id = q2_opp_id[0]
                    if not q2_opp_id:
                        oppoertunity_Obj.create({'lead_id': opp_id,
                                                 'ref_id': q2_seller_id.id,
                                                 })
                # lead Line Creation #
                for lead_id in seller_q2_lead_count:
                    q2_lead_id = lead_Obj.search([('ref_id', '=', q2_seller_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q2_lead_id) > 1:
                        q2_lead_id = q2_lead_id[0]
                    if not q2_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q2_seller_id.id,
                                         })

                q3_seller_id = seller_oppObj.search([('ref_id', '=', q3_pipeline_build_id.id),
                                                     ('fiscalyear_id', '=', fiscalyear_id.id),
                                                     ('sales_target_user', '=', fields_user.id)])
                if len(q3_seller_id) > 1:
                    q3_seller_id = q3_seller_id[0]
                if not q3_seller_id:
                    q3_seller_id = seller_oppObj.create({'sales_target_user': fields_user.id,
                                                         'fiscalyear_id': fiscalyear_id.id,
                                                         'opportunity_count': len(seller_q3_opp_count),
                                                         'opportunity_value': seller_q3_pipe_value,
                                                         'lead_count': len(seller_q3_lead_count),
                                                         'ref_id': q3_pipeline_build_id.id})
                else:
                    q3_seller_id.opportunity_count = len(seller_q3_opp_count)
                    q3_seller_id.opportunity_value = seller_q3_pipe_value
                    q3_seller_id.lead_count = len(seller_q3_lead_count)

                if q3_seller_id.sales_target_user.manager_user_relation_id.user_id:
                    q3_seller_id.sales_manager = q3_seller_id.sales_target_user.manager_user_relation_id.user_id.id

                for opp_id in seller_q3_opp_count:
                    q3_opp_id = oppoertunity_Obj.search([('ref_id', '=', q3_seller_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q3_opp_id) > 1:
                        q3_opp_id = q3_opp_id[0]
                    if not q3_opp_id:
                        oppoertunity_Obj.create({'lead_id': opp_id,
                                                 'ref_id': q3_seller_id.id,
                                                 })
                # lead Line Creation #
                for lead_id in seller_q3_lead_count:
                    q3_lead_id = lead_Obj.search([('ref_id', '=', q3_seller_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q3_lead_id) > 1:
                        q3_lead_id = q3_lead_id[0]
                    if not q3_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q3_seller_id.id,
                                         })

                q4_seller_id = seller_oppObj.search([('ref_id', '=', q4_pipeline_build_id.id),
                                                     ('fiscalyear_id', '=', fiscalyear_id.id),
                                                     ('sales_target_user', '=', fields_user.id)])
                if len(q4_seller_id) > 1:
                    q4_seller_id = q4_seller_id[0]
                if not q4_seller_id:
                    q4_seller_id = seller_oppObj.create({'sales_target_user': fields_user.id,
                                                         'fiscalyear_id': fiscalyear_id.id,
                                                         'opportunity_count': len(seller_q4_opp_count),
                                                         'opportunity_value': seller_q4_pipe_value,
                                                         'lead_count': len(seller_q4_lead_count),
                                                         'ref_id': q4_pipeline_build_id.id})
                else:
                    q4_seller_id.opportunity_count = len(seller_q4_opp_count)
                    q4_seller_id.opportunity_value = seller_q4_pipe_value
                    q4_seller_id.lead_count = len(seller_q4_lead_count)

                if q4_seller_id.sales_target_user.manager_user_relation_id.user_id:
                    q4_seller_id.sales_manager = q4_seller_id.sales_target_user.manager_user_relation_id.user_id.id

                for opp_id in seller_q4_opp_count:
                    q4_opp_id = oppoertunity_Obj.search([('ref_id', '=', q4_seller_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q4_opp_id) > 1:
                        q4_opp_id = q4_opp_id[0]
                    if not q4_opp_id:
                        oppoertunity_Obj.create({'lead_id': opp_id,
                                                 'ref_id': q4_seller_id.id,
                                                })
                # lead Line Creation #
                for lead_id in seller_q4_lead_count:
                    q4_lead_id = lead_Obj.search([('ref_id', '=', q4_seller_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q4_lead_id) > 1:
                        q4_lead_id = q4_lead_id[0]
                    if not q4_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q4_seller_id.id,
                                         })
                seller_q1_opp_count[:] = []
                seller_q2_opp_count[:] = []
                seller_q3_opp_count[:] = []
                seller_q4_opp_count[:] = []
                seller_q1_lead_count[:] = []
                seller_q2_lead_count[:] = []
                seller_q3_lead_count[:] = []
                seller_q4_lead_count[:] = []


class bu_opportunity_line(models.Model):
    _name = 'bu.opportunity.line'
    _description = 'BU Opportunity Line'
    _order = "id desc"

    AVAILABLE_STAGES = [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'Aug'),
        ('9', 'Sept'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),
    ]

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    lead_id = fields.Many2one('crm.lead', 'Opportunity Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Date', related="lead_id.partner_id", store=True, readonly=True)
    date_deadline = fields.Date('Expected Closing', related="lead_id.date_deadline", store=True, readonly=True)
    date_converted = fields.Date('Opportunity Converted Date', related="lead_id.date_converted", store=True, readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", readonly=True)
    bu_revenue = fields.Float('BU OrderBooking', related="lead_id.bu_revenue", readonly=True)
    bu_revenue_for = fields.Char('BU OrderBooking For', related="lead_id.bu_revenue_for", readonly=True)
    multi_dept = fields.Boolean('Is Multi Department', related="lead_id.multi_dept",store=True,readonly=True) 
    stage_id = fields.Many2one('crm.case.stage', 'Stage', related="lead_id.stage_id",store=True, readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="lead_id.country_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_opportunity_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('bu.quarter.pipeline.build', 'Reference', readonly=True)

    title_action = fields.Char('Title Action', related="lead_id.title_action", store=True, readonly=True)
    is_omm_mismatch = fields.Boolean('OMM Mismatch', related="lead_id.is_omm_mismatch", store=True, readonly=True)
    date_action = fields.Date('Date Action', related="lead_id.date_action", store=True, readonly=True)
    omm_id = fields.Many2one('crm.omm', 'OMM Register', related="lead_id.omm_id", store=True, readonly=True)
    seller_call_deal = fields.Selection(AVAILABLE_STAGES, 'Seller Call Deal Month', related="lead_id.seller_call_deal",
                                        store=True, readonly=True)
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Seller Call Deal Quarter',
                                         related="lead_id.call_deal_quarter", store=True, readonly=True)
    bu_call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'BU Call Deal Quarter',
                                            related="lead_id.bu_call_deal_quarter", store=True, readonly=True)
    bu_call_deal = fields.Selection(AVAILABLE_STAGES, 'BU Call Deal Month', related="lead_id.bu_call_deal", store=True,
                                    readonly=True)


class bu_lead_line(models.Model):
    _name = 'bu.lead.line'
    _description = 'BU Lead Line'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Date', related="lead_id.partner_id", store=True, readonly=True)
    date_deadline = fields.Date('Expected Closing', related="lead_id.date_deadline", store=True, readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage', related="lead_id.stage_id", store=True, readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="lead_id.country_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_lead_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('bu.quarter.pipeline.build', 'Reference', readonly=True)

    is_omm_mismatch = fields.Boolean('OMM Mismatch', related="lead_id.is_omm_mismatch", store=True, readonly=True)
    omm_id = fields.Many2one('crm.omm', 'OMM Register', related="lead_id.omm_id", store=True, readonly=True)


class bu_quarter_pipeline_build(models.Model):
    _name = 'bu.quarter.pipeline.build'
    _description = 'BU Quarter Pipeline Build'
    _rec_name = 'name'
    _order = 'name'

    @api.one
    @api.depends('pipeline_build_value', 'opportunity_value')
    def _pipeline_build_achievement(self):
        if self.pipeline_build_value and self.opportunity_value:
            self.pipeline_build_achievement = (self.opportunity_value * 100 / self.pipeline_build_value)
        self.pipeline_build_variant = float(self.opportunity_value) - float(self.pipeline_build_value)

    name = fields.Char('Quarter', readonly=True)
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Integer('Pipeline Build Achievement', readonly=True)
    lead_count = fields.Integer('Lead Count', readonly=True)
    pipeline_build_value = fields.Integer('Pipeline Build Target', readonly=False)
    pipeline_build_variant = fields.Integer('Pipeline Build Variant', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    pipeline_build_achievement = fields.Integer('Pipeline Build Achievement %', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    opportunity_line = fields.One2many('bu.opportunity.line', 'ref_id', 'BU Opportunity Line', readonly=True)
    lead_line = fields.One2many('bu.lead.line', 'ref_id', 'BU Lead Line', readonly=True)
    ref_id = fields.Many2one('bu.pipeline.build', 'Business Unit', readonly=True)


class bu_pipeline_build(models.Model):
    _name = 'bu.pipeline.build'
    _description = 'BU Pipeline Build'
    _rec_name = 'department_id'
    _order = 'department_id'

    @api.one
    @api.depends('pipeline_build_value', 'opportunity_value')
    def _pipeline_build_achievement(self):
        if self.pipeline_build_value and self.opportunity_value:
            self.pipeline_build_achievement = (self.opportunity_value * 100 / self.pipeline_build_value)
        self.pipeline_build_variant = float(self.opportunity_value) - float(self.pipeline_build_value)

    @api.one
    @api.depends('quarter_line')
    def update_quarter_wise_values(self):
        q1_pipeline_target = 0
        q2_pipeline_target = 0
        q3_pipeline_target = 0
        q4_pipeline_target = 0
        q1_pipeline_achievement = 0
        q2_pipeline_achievement = 0
        q3_pipeline_achievement = 0
        q4_pipeline_achievement = 0
        if self.quarter_line:
            for quarter_line in self.quarter_line:
                if quarter_line.name == 'Q1 (AMJ)':
                    q1_pipeline_target = quarter_line.pipeline_build_value
                    q1_pipeline_achievement = quarter_line.opportunity_value
                elif quarter_line.name == 'Q2 (JAS)':
                    q2_pipeline_target = quarter_line.pipeline_build_value
                    q2_pipeline_achievement = quarter_line.opportunity_value
                elif quarter_line.name == 'Q3 (OND)':
                    q3_pipeline_target = quarter_line.pipeline_build_value
                    q3_pipeline_achievement = quarter_line.opportunity_value
                elif quarter_line.name == 'Q4 (JFM)':
                    q4_pipeline_target = quarter_line.pipeline_build_value
                    q4_pipeline_achievement = quarter_line.opportunity_value
                else:
                    pass
            self.q1_pipeline_target = q1_pipeline_target
            self.q1_pipeline_achievement = q1_pipeline_achievement
            self.q2_pipeline_target = q2_pipeline_target
            self.q2_pipeline_achievement = q2_pipeline_achievement
            self.q3_pipeline_target = q3_pipeline_target
            self.q3_pipeline_achievement = q3_pipeline_achievement
            self.q4_pipeline_target = q4_pipeline_target
            self.q4_pipeline_achievement = q4_pipeline_achievement

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Integer('Pipeline Build Achievement', readonly=True)
    lead_count = fields.Integer('Lead Count', readonly=True)
    pipeline_build_value = fields.Integer('Pipeline Build Target', readonly=False)
    pipeline_build_variant = fields.Integer('Pipeline Build variant', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    pipeline_build_achievement = fields.Integer('Pipeline Build Achievement %', compute='_pipeline_build_achievement',
                                                store=True, readonly=True)
    q1_pipeline_target = fields.Integer('Q1 Pipeline Target', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q2_pipeline_target = fields.Integer('Q2 Pipeline Target', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q3_pipeline_target = fields.Integer('Q3 Pipeline Target', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q4_pipeline_target = fields.Integer('Q4 Pipeline Target', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q1_pipeline_achievement = fields.Integer('Q1 Pipeline Achievement', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q2_pipeline_achievement = fields.Integer('Q2 Pipeline Achievement', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q3_pipeline_achievement = fields.Integer('Q3 Pipeline Achievement', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    q4_pipeline_achievement = fields.Integer('Q4 Pipeline Achievement', compute='update_quarter_wise_values',
                                                store=True, readonly=True)
    quarter_line = fields.One2many('bu.quarter.pipeline.build', 'ref_id', 'BU Quarter Pipeline Build Line', readonly=False)
    color = fields.Integer('Colour', default=6)

    @api.model
    def run_bu_opportunity_pipeline_build(self):
        selfObj = self.env['bu.pipeline.build']
        crmLeadObj = self.env['crm.lead']
        case_stageObj = self.env['crm.case.stage']
        lead_Obj = self.env['bu.lead.line']
        opportunity_Obj = self.env['bu.opportunity.line']
        quarter_Obj = self.env['bu.quarter.pipeline.build']
        current_date = datetime.date.today()
        ninety_end_date = datetime.date.today() + timedelta(days=90)
        stage_list = []
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])
        if stage_ids:
            for stage in stage_ids:
                stage_list.append(stage.id)
        lead_stages_list = []
        lead_stages_ids = case_stageObj.search([('type', '=', 'lead')])
        if lead_stages_ids:
            for stage in lead_stages_ids:
                lead_stages_list.append(stage.id)
        fiscalyear_id = None
        fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                ('date_stop', '>=', current_date)])
        bu_list = []
        total_pipe_value = {}
        total_opp_count = {}
        total_lead_count = {}
        q1_pipe_value = {}
        q2_pipe_value = {}
        q3_pipe_value = {}
        q4_pipe_value = {}
        q1_opp_count = {}
        q2_opp_count = {}
        q3_opp_count = {}
        q4_opp_count = {}
        q1_lead_count = {}
        q2_lead_count = {}
        q3_lead_count = {}
        q4_lead_count = {}
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
            bu_revenue_lineObj = self.env['crm.lead.revenue.ratio']
            bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
            for bu in bu_ids:
                bu_id = None
                if bu.parent:
                    bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                    if bu_child:
                        bu_id = bu_child[0].id
                else:
                    bu_id = bu.id
                if bu_id not in bu_list:
                    bu_list.append(bu_id)
                for lead_id in crmLeadObj.search([('create_date', '>=', q1_start_date),
                                                  ('create_date', '<=', q1_end_date),
                                                  ('department_id', '=', bu.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    if bu_id not in q1_lead_count:
                        q1_lead_count[bu_id] = []
                    q1_lead_count[bu_id].append(lead_id.id)

                    if bu_id not in total_lead_count:
                        total_lead_count[bu_id] = []
                    total_lead_count[bu_id].append(lead_id.id)

                for lead_id in crmLeadObj.search([('create_date', '>=', q2_start_date),
                                                  ('create_date', '<=', q2_end_date),
                                                  ('department_id', '=', bu.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    if bu_id not in q2_lead_count:
                        q2_lead_count[bu_id] = []
                    q2_lead_count[bu_id].append(lead_id.id)

                    if bu_id not in total_lead_count:
                        total_lead_count[bu_id] = []
                    total_lead_count[bu_id].append(lead_id.id)

                for lead_id in crmLeadObj.search([('create_date', '>=', q3_start_date),
                                                  ('create_date', '<=', q3_end_date),
                                                  ('department_id', '=', bu.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    if bu_id not in q3_lead_count:
                        q3_lead_count[bu_id] = []
                    q3_lead_count[bu_id].append(lead_id.id)

                    if bu_id not in total_lead_count:
                        total_lead_count[bu_id] = []
                    total_lead_count[bu_id].append(lead_id.id)

                for lead_id in crmLeadObj.search([('create_date', '>=', q4_start_date),
                                                  ('create_date', '<=', q4_end_date),
                                                  ('department_id', '=', bu.id),
                                                  ('stage_id', 'in', lead_stages_list)]):
                    if bu_id not in q4_lead_count:
                        q4_lead_count[bu_id] = []
                    q4_lead_count[bu_id].append(lead_id.id)

                    if bu_id not in total_lead_count:
                        total_lead_count[bu_id] = []
                    total_lead_count[bu_id].append(lead_id.id)
                    
                    
                #Q1 Dictionary here
                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q1_start_date),
                                                         ('date_converted', '<=', q1_end_date),
                                                         ('stage_id', 'in', stage_list)]):
                    if opportunity_id.multi_dept:
                        bu_revenue_ids = bu_revenue_lineObj.search([('department_id','=',bu.id),('lead_id','=',opportunity_id.id)])
                        if bu_revenue_ids:
                            for bu_line_id in bu_revenue_ids:
                                if bu_line_id.department_id.id:
                                    #bu_id = bu_line_id.department_id
                                    if bu_id not in q1_pipe_value:
                                        q1_pipe_value[bu_id] = 0.0
                                    if bu_id in q1_pipe_value:    
                                        q1_pipe_value[bu_id] += bu_line_id.planned_revenue
                                    if bu_id not in q1_opp_count:
                                        q1_opp_count[bu_id] = []
                                    q1_opp_count[bu_id].append(opportunity_id.id)

                                    if bu_id not in total_pipe_value:
                                        total_pipe_value[bu_id] = 0.0
                                    total_pipe_value[bu_id] += bu_line_id.planned_revenue

                                    if bu_id not in total_opp_count:
                                        total_opp_count[bu_id] = []
                                    total_opp_count[bu_id].append(opportunity_id.id)
                        else:
                            pass
                    else:
                        if opportunity_id.department_id.id == bu.id:
                            if bu_id not in q1_pipe_value:
                                q1_pipe_value[bu_id] = 0.0
                            #Hided by Praveen and replaced in all places inside this method    
                            #q1_pipe_value[bu_id] += opportunity_id.planned_revenue
                            if bu_id in q1_pipe_value: 
                                q1_pipe_value[bu_id] += opportunity_id.bu_revenue
                            if bu_id not in q1_opp_count:
                                q1_opp_count[bu_id] = []
                            q1_opp_count[bu_id].append(opportunity_id.id)

                            if bu_id not in total_pipe_value:
                                total_pipe_value[bu_id] = 0.0
                            total_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in total_opp_count:
                                total_opp_count[bu_id] = []
                            total_opp_count[bu_id].append(opportunity_id.id)
                        else:
                            pass

                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q2_start_date),
                                                         ('date_converted', '<=', q2_end_date),
                                                         ('stage_id', 'in', stage_list)]):
                    if opportunity_id.multi_dept:
                        for bu_line_id in opportunity_id.revenue_ratio_line:

                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q2_pipe_value:
                                    q2_pipe_value[bu_id] = 0.0
                                q2_pipe_value[bu_id] += bu_line_id.planned_revenue

                                if bu_id not in q2_opp_count:
                                    q2_opp_count[bu_id] = []
                                q2_opp_count[bu_id].append(opportunity_id.id)

                                if bu_id not in total_pipe_value:
                                    total_pipe_value[bu_id] = 0.0
                                total_pipe_value[bu_id] += bu_line_id.planned_revenue

                                if bu_id not in total_opp_count:
                                    total_opp_count[bu_id] = []
                                total_opp_count[bu_id].append(opportunity_id.id)
                            else:
                                pass
                            #print "what in Q2 pipe value",q2_pipe_value,opportunity_id.name

                    else:
                        if opportunity_id.department_id.id == bu.id:
                            if bu_id not in q2_pipe_value:
                                q2_pipe_value[bu_id] = 0.0
                            q2_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in q2_opp_count:
                                q2_opp_count[bu_id] = []
                            q2_opp_count[bu_id].append(opportunity_id.id)

                            if bu_id not in total_pipe_value:
                                total_pipe_value[bu_id] = 0.0
                            total_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in total_opp_count:
                                total_opp_count[bu_id] = []
                            total_opp_count[bu_id].append(opportunity_id.id)
                        else:
                            pass
                    
                    
                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q3_start_date),
                                                         ('date_converted', '<=', q3_end_date),
                                                         ('stage_id', 'in', stage_list)]):
                    if opportunity_id.multi_dept:
                        for bu_line_id in opportunity_id.revenue_ratio_line:

                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q3_pipe_value:
                                    q3_pipe_value[bu_id] = 0.0
                                q3_pipe_value[bu_id] += opportunity_id.bu_revenue

                                if bu_id not in q3_opp_count:
                                    q3_opp_count[bu_id] = []
                                q3_opp_count[bu_id].append(opportunity_id.id)

                                if bu_id not in total_pipe_value:
                                    total_pipe_value[bu_id] = 0.0
                                total_pipe_value[bu_id] += bu_line_id.planned_revenue

                                if bu_id not in total_opp_count:
                                    total_opp_count[bu_id] = []
                                total_opp_count[bu_id].append(opportunity_id.id)
                            else:
                                pass
                    else:
                        if opportunity_id.department_id.id == bu.id:
                            if bu_id not in q3_pipe_value:
                                q3_pipe_value[bu_id] = 0.0
                            q3_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in q3_opp_count:
                                q3_opp_count[bu_id] = []
                            q3_opp_count[bu_id].append(opportunity_id.id)

                            if bu_id not in total_pipe_value:
                                total_pipe_value[bu_id] = 0.0
                            total_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in total_opp_count:
                                total_opp_count[bu_id] = []
                            total_opp_count[bu_id].append(opportunity_id.id)
                        else:
                            pass

                for opportunity_id in crmLeadObj.search([('date_converted', '>=', q4_start_date),
                                                         ('date_converted', '<=', q4_end_date),
                                                         ('stage_id', 'in', stage_list)]):
                    if opportunity_id.multi_dept:
                        for bu_line_id in opportunity_id.revenue_ratio_line:

                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q4_pipe_value:
                                    q4_pipe_value[bu_id] = 0.0
                                q4_pipe_value[bu_id] += opportunity_id.bu_revenue

                                if bu_id not in q4_opp_count:
                                    q4_opp_count[bu_id] = []
                                q4_opp_count[bu_id].append(opportunity_id.id)

                                if bu_id not in total_pipe_value:
                                    total_pipe_value[bu_id] = 0.0
                                total_pipe_value[bu_id] += bu_line_id.planned_revenue

                                if bu_id not in total_opp_count:
                                    total_opp_count[bu_id] = []
                                total_opp_count[bu_id].append(opportunity_id.id)
                            else:
                                pass
                    else:
                        if opportunity_id.department_id.id == bu.id:
                            if bu_id not in q4_pipe_value:
                                q4_pipe_value[bu_id] = 0.0
                            q4_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in q4_opp_count:
                                q4_opp_count[bu_id] = []
                            q4_opp_count[bu_id].append(opportunity_id.id)

                            if bu_id not in total_pipe_value:
                                total_pipe_value[bu_id] = 0.0
                            total_pipe_value[bu_id] += opportunity_id.bu_revenue

                            if bu_id not in total_opp_count:
                                total_opp_count[bu_id] = []
                            total_opp_count[bu_id].append(opportunity_id.id)
                        else:
                            pass

                    ################################################

            for bu in bu_list:
            # # Creating or updating BU pipeline built # #
                bu_record = selfObj.search([('fiscalyear_id', '=', fiscalyear_id.id), ('department_id', '=', bu)])
                if bu not in total_opp_count:
                    opp_count = 0
                else:
                    opp_count = len(total_opp_count[bu])
                if bu not in total_lead_count:
                    lead_count = 0
                else:
                    lead_count = len(total_lead_count[bu])
                if bu not in total_pipe_value:
                    opportunity_value = 0
                else:
                    opportunity_value = total_pipe_value[bu]

                if not bu_record:
                    bu_record = selfObj.create({'department_id': bu,
                                                'fiscalyear_id': fiscalyear_id.id,
                                                'opportunity_count': opp_count,
                                                'opportunity_value': opportunity_value,
                                                'lead_count': lead_count,
                                                })
                else:

                    bu_record.opportunity_value = opportunity_value
                    bu_record.opportunity_count = opp_count
                    bu_record.lead_count = lead_count

                q1_pipeline_build_id = quarter_Obj.search([('ref_id', '=', bu_record.id), ('name', '=', 'Q1 (AMJ)')])
                if len(q1_pipeline_build_id) > 1:
                    q1_pipeline_build_id = q1_pipeline_build_id[0]
                if bu not in q1_opp_count:
                    bu_q1_opportunity_count = []
                else:
                    bu_q1_opportunity_count = q1_opp_count[bu]
                if bu not in q1_lead_count:
                    bu_q1_lead_count = []
                else:
                    bu_q1_lead_count = q1_lead_count[bu]
                if bu not in q1_pipe_value:
                    bu_q1_opportunity_value = 0
                else:
                    bu_q1_opportunity_value = q1_pipe_value[bu]

                if not q1_pipeline_build_id:
                    q1_pipeline_build_id = quarter_Obj.create({'name': 'Q1 (AMJ)',
                                                                'fiscalyear_id': fiscalyear_id.id,
                                                                'opportunity_count': len(bu_q1_opportunity_count),
                                                                'opportunity_value': bu_q1_opportunity_value,
                                                                'lead_count': len(bu_q1_lead_count),
                                                               'ref_id': bu_record.id,
                                                               })
                else:
                    #print "what comign in q1 part",bu_q1_opportunity_value,bu_record.id
                    q1_pipeline_build_id.opportunity_value = bu_q1_opportunity_value
                    q1_pipeline_build_id.opportunity_count = len(bu_q1_opportunity_count)
                    q1_pipeline_build_id.lead_count = len(bu_q1_lead_count)

                # Q1 BU Opportunity Line Creation #
                for opp_id in bu_q1_opportunity_count:
                    q1_opp_id = opportunity_Obj.search([('ref_id', '=', q1_pipeline_build_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q1_opp_id) > 1:
                        q1_opp_id = q1_opp_id[0]
                    if not q1_opp_id:
                        opportunity_Obj.create({'lead_id': opp_id,
                                                'ref_id': q1_pipeline_build_id.id,
                                                })

                # Q1 BU Lead Line Creation #
                for lead_id in bu_q1_lead_count:
                    q1_lead_id = lead_Obj.search([('ref_id', '=', q1_pipeline_build_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q1_lead_id) > 1:
                        q1_lead_id = q1_lead_id[0]
                    if not q1_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q1_pipeline_build_id.id,
                                         })

                q2_pipeline_build_id = quarter_Obj.search([('ref_id', '=', bu_record.id), ('name', '=', 'Q2 (JAS)')])
                if len(q2_pipeline_build_id) > 1:
                    q2_pipeline_build_id = q2_pipeline_build_id[0]
                if bu not in q2_opp_count:
                    bu_q2_opportunity_count = []
                else:
                    bu_q2_opportunity_count = q2_opp_count[bu]
                if bu not in q2_lead_count:
                    bu_q2_lead_count = []
                else:
                    bu_q2_lead_count = q2_lead_count[bu]
                if bu not in q2_pipe_value:
                    bu_q2_opportunity_value = 0
                else:
                    bu_q2_opportunity_value = q2_pipe_value[bu]

                if not q2_pipeline_build_id:
                    q2_pipeline_build_id = quarter_Obj.create({'name': 'Q2 (JAS)',
                                                                'fiscalyear_id': fiscalyear_id.id,
                                                                'opportunity_count': len(bu_q2_opportunity_count),
                                                                'opportunity_value': bu_q2_opportunity_value,
                                                                'lead_count': len(bu_q2_lead_count),
                                                               'ref_id': bu_record.id,
                                                               })
                else:
                    q2_pipeline_build_id.opportunity_value = bu_q2_opportunity_value
                    q2_pipeline_build_id.opportunity_count = len(bu_q2_opportunity_count)
                    q2_pipeline_build_id.lead_count = len(bu_q2_lead_count)

                # Q2 BU Opportunity Line Creation #
                for opp_id in bu_q2_opportunity_count:
                    q2_opp_id = opportunity_Obj.search([('ref_id', '=', q2_pipeline_build_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q2_opp_id) > 1:
                        q2_opp_id = q2_opp_id[0]
                    if not q2_opp_id:
                        opportunity_Obj.create({'lead_id': opp_id,
                                                'ref_id': q2_pipeline_build_id.id,
                                                })
                # Q2 BU Lead Line Creation #
                for lead_id in bu_q2_lead_count:
                    q2_lead_id = lead_Obj.search([('ref_id', '=', q2_pipeline_build_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q2_lead_id) > 1:
                        q2_lead_id = q2_lead_id[0]
                    if not q2_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q2_pipeline_build_id.id,
                                         })

                q3_pipeline_build_id = quarter_Obj.search([('ref_id', '=', bu_record.id), ('name', '=', 'Q3 (OND)')])
                if len(q3_pipeline_build_id) > 1:
                    q3_pipeline_build_id = q3_pipeline_build_id[0]
                if bu not in q3_opp_count:
                    bu_q3_opportunity_count = []
                else:
                    bu_q3_opportunity_count = q3_opp_count[bu]
                if bu not in q3_lead_count:
                    bu_q3_lead_count = []
                else:
                    bu_q3_lead_count = q3_lead_count[bu]
                if bu not in q4_pipe_value:
                    bu_q3_opportunity_value = 0
                else:
                    bu_q3_opportunity_value = q3_pipe_value[bu]

                if not q3_pipeline_build_id:
                    q3_pipeline_build_id = quarter_Obj.create({'name': 'Q3 (OND)',
                                                                'fiscalyear_id': fiscalyear_id.id,
                                                                'opportunity_count': len(bu_q3_opportunity_count),
                                                                'opportunity_value': bu_q3_opportunity_value,
                                                                'lead_count': len(bu_q3_lead_count),
                                                               'ref_id': bu_record.id,
                                                               })
                else:
                    q3_pipeline_build_id.opportunity_value = bu_q3_opportunity_value
                    q3_pipeline_build_id.opportunity_count = len(bu_q3_opportunity_count)
                    q3_pipeline_build_id.lead_count = len(bu_q3_lead_count)

                # Q3 BU Opportunity Line Creation #
                for opp_id in bu_q3_opportunity_count:
                    q3_opp_id = opportunity_Obj.search([('ref_id', '=', q3_pipeline_build_id.id),
                                                         ('lead_id', '=', opp_id)])
                    if len(q3_opp_id) > 1:
                        q3_opp_id = q3_opp_id[0]
                    if not q3_opp_id:
                        opportunity_Obj.create({'lead_id': opp_id,
                                                 'ref_id': q3_pipeline_build_id.id,
                                                 })
                # Q3 BU Lead Line Creation #
                for lead_id in bu_q3_lead_count:
                    q3_lead_id = lead_Obj.search([('ref_id', '=', q3_pipeline_build_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q3_lead_id) > 1:
                        q3_lead_id = q3_lead_id[0]
                    if not q3_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q3_pipeline_build_id.id,
                                         })

                q4_pipeline_build_id = quarter_Obj.search([('ref_id', '=', bu_record.id), ('name', '=', 'Q4 (JFM)')])
                if len(q4_pipeline_build_id) > 1:
                    q4_pipeline_build_id = q4_pipeline_build_id[0]
                if bu not in q4_opp_count:
                    bu_q4_opportunity_count = []
                else:
                    bu_q4_opportunity_count = q4_opp_count[bu]
                if bu not in q4_lead_count:
                    bu_q4_lead_count = []
                else:
                    bu_q4_lead_count = q4_lead_count[bu]
                if bu not in q4_pipe_value:
                    bu_q4_opportunity_value = 0
                else:
                    bu_q4_opportunity_value = q4_pipe_value[bu]

                if not q4_pipeline_build_id:
                    q4_pipeline_build_id = quarter_Obj.create({'name': 'Q4 (JFM)',
                                                                'fiscalyear_id': fiscalyear_id.id,
                                                                'opportunity_count': len(bu_q4_opportunity_count),
                                                                'opportunity_value': bu_q4_opportunity_value,
                                                                'lead_count': len(bu_q4_lead_count),
                                                               'ref_id': bu_record.id,
                                                               })
                else:
                    q4_pipeline_build_id.opportunity_value = bu_q4_opportunity_value
                    q4_pipeline_build_id.opportunity_count = len(bu_q4_opportunity_count)
                    q4_pipeline_build_id.lead_count = len(bu_q4_lead_count)

                # Q4 BU Opportunity Line Creation #
                for opp_id in bu_q4_opportunity_count:
                    q4_opp_id = opportunity_Obj.search([('ref_id', '=', q4_pipeline_build_id.id),
                                                        ('lead_id', '=', opp_id)])
                    if len(q4_opp_id) > 1:
                        q4_opp_id = q4_opp_id[0]
                    if not q4_opp_id:
                        opportunity_Obj.create({'lead_id': opp_id,
                                                'ref_id': q4_pipeline_build_id.id,
                                                })
                # Q4 BU Lead Line Creation #
                for lead_id in bu_q4_lead_count:
                    q4_lead_id = lead_Obj.search([('ref_id', '=', q4_pipeline_build_id.id),
                                                  ('lead_id', '=', lead_id)])
                    if len(q4_lead_id) > 1:
                        q4_lead_id = q4_lead_id[0]
                    if not q4_lead_id:
                        lead_Obj.create({'lead_id': lead_id,
                                         'ref_id': q4_pipeline_build_id.id,
                                         })


class opportunity_slipups_log(models.Model):
    _name = 'opportunity.slipups.log'
    _description = 'Opportunity Slip ups Log'
    _order = "id desc"

    AVAILABLE_STAGES = [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'Aug'),
        ('9', 'Sept'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),
    ]

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="opportunity_id.name", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="opportunity_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="opportunity_id.department_id", store=True,
                                    readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', related="opportunity_id.partner_id", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage', readonly=True)
    zebra_rating = fields.Float('Zebra Score', readonly=True)
    date_deadline = fields.Date('Expected Closing', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="opportunity_id.country_id", store=True, readonly=True)
    seller_call_deal = fields.Selection(AVAILABLE_STAGES, 'Seller Call Deal Month', readonly=True)
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Seller Call Deal Quarter', readonly=True)
    bu_call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'BU Call Deal Quarter', readonly=True)
    bu_call_deal = fields.Selection(AVAILABLE_STAGES, 'BU Call Deal Month', readonly=True)
    ref_id = fields.Many2one('crm.lead', 'Reference', readonly=True)


class opportunity_slippage_log(models.Model):
    _name = 'opportunity.slippage.log'
    _description = 'Opportunity Slippage Log'
    _order = "id desc"

    AVAILABLE_STAGES = [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'Aug'),
        ('9', 'Sept'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),
    ]

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity Reference', readonly=True)
    name = fields.Char('Opportunity Name', related="opportunity_id.name", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Field SalesPerson', related="opportunity_id.user_id", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="opportunity_id.department_id", store=True,
                                    readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', related="opportunity_id.partner_id", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage', readonly=True)
    zebra_rating = fields.Float('Zebra Score', readonly=True)
    date_deadline = fields.Date('Expected Closing', readonly=True)
    country_id = fields.Many2one('res.country', 'Country', related="opportunity_id.country_id", store=True, readonly=True)
    seller_call_deal = fields.Selection(AVAILABLE_STAGES, 'Seller Call Deal Month', readonly=True)
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Seller Call Deal Quarter', readonly=True)
    bu_call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'BU Call Deal Quarter', readonly=True)
    bu_call_deal = fields.Selection(AVAILABLE_STAGES, 'BU Call Deal Month', readonly=True)
    ref_id = fields.Many2one('crm.lead', 'Reference', readonly=True)


class crm_lead(models.Model):
    _inherit = 'crm.lead'
    _order = "department_id, planned_revenue desc,id desc"

    AVAILABLE_STAGES = [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'Aug'),
        ('9', 'Sept'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),
    ]

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    @api.one
    @api.depends('seller_call_deal', 'bu_call_deal')
    def _call_deal(self):
        if self.seller_call_deal:
            if self.seller_call_deal in ('4', '5', '6'):
                self.call_deal_quarter = '1'
            elif self.seller_call_deal in ('7', '8', '9'):
                self.call_deal_quarter = '2'
            elif self.seller_call_deal in ('10', '11', '12'):
                self.call_deal_quarter = '3'
            elif self.seller_call_deal in ('1', '2', '3'):
                self.call_deal_quarter = '4'
            else:
                self.call_deal_quarter = ''
        if self.bu_call_deal:
            if self.bu_call_deal in ('4', '5', '6'):
                self.bu_call_deal_quarter = '1'
            elif self.bu_call_deal in ('7', '8', '9'):
                self.bu_call_deal_quarter = '2'
            elif self.bu_call_deal in ('10', '11', '12'):
                self.bu_call_deal_quarter = '3'
            elif self.bu_call_deal in ('1', '2', '3'):
                self.bu_call_deal_quarter = '4'
            else:
                self.bu_call_deal_quarter = ''

    @api.one
    @api.depends('date_deadline')
    def _delay_days_calculation(self):
        lead_deltaObj = self.env['crm.lead.delta']
        delta_closures_previous = lead_deltaObj.search([('crm_lead_id', '=', self.id)])
        difference = 0
        today = fields.datetime.now()
        if self.date_deadline:
            updated_closures_date = datetime.datetime.strptime(self.date_deadline, "%Y-%m-%d")
            if today > updated_closures_date:
                raise exceptions.ValidationError("Expected Closing Date Should be greater than today\'s date")
        if delta_closures_previous:
            if delta_closures_previous[0].date_deadline:
                previous_closures_date = datetime.datetime.strptime(delta_closures_previous[0].date_deadline, "%Y-%m-%d")
                # updated_closures_date = datetime.datetime.strptime(self.date_deadline, "%Y-%m-%d")
                difference = int((updated_closures_date - previous_closures_date).days)
                if not difference > 0:
                    difference = 0
        self.lead_delay_days = difference

    seller_call_deal = fields.Selection(AVAILABLE_STAGES, 'Seller Call Deal Month')
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Seller Call Deal Quarter', compute='_call_deal', store=True,
                                         readonly=True)
    bu_call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'BU Call Deal Quarter', compute='_call_deal', store=True,
                                         readonly=True)
    bu_call_deal = fields.Selection(AVAILABLE_STAGES, 'BU Call Deal Month')
    seller_check = fields.Boolean('Check call deal to readonly for Seller')
    focus_deal = fields.Selection([('YES', 'YES'), ('NO', 'NO')], 'Focus Deal')
    is_omm_mismatch = fields.Boolean('OMM Mismatch', readonly=True)
    lead_delay_days = fields.Integer('Delay Days', compute='_delay_days_calculation', store=True, readonly=True)
    bu_check = fields.Boolean('Check call deal to readonly for BU')
    ninety_days = fields.Boolean('Is in coming 90 days?', readonly=True)
    wlo_opportunities = fields.Boolean('Is Win/Loss/Onhold?', readonly=True)
    this_year = fields.Boolean('This Fiscal Year', readonly=True)
    slippage = fields.Boolean('Show in Slippage', readonly=False)
    show_call_deals = fields.Boolean('Show in Call Deals', readonly=False)
    case_stage_type = fields.Selection('CRM Stage Type', related='stage_id.type', store=True, readonly=True)
    from_gss_menu = fields.Boolean('GSS Menu', default=False)
    bu_revenue = fields.Float('BU OrderBooking')
    bu_revenue_for = fields.Char('BU OrderBooking For')
    planned_revenue = fields.Float('Expected OrderBooking', track_visibility='always')
    slipups_log_ids = fields.One2many('opportunity.slipups.log', 'ref_id', 'Opportunity Slip-ups Log', readonly=True)
    slippage_log_ids = fields.One2many('opportunity.slippage.log', 'ref_id', 'Opportunity Slippage Log', readonly=True)

    @api.one
    def write(self, vals):
        crm_id = super(crm_lead, self).write(vals)
        list = ['bu_call_deal', 'seller_call_deal']
        count = 0
        for value in list:
            if value in vals:
                count += 1

        if self.slippage:
            if count > 0 or 'date_deadline' in vals:
                slippage_log_id = self.env['opportunity.slippage.log'].create({'opportunity_id': self.id,
                                                                               'seller_call_deal': self.seller_call_deal,
                                                                               'zebra_rating': self.zebra_rating,
                                                                               'date_deadline': self.date_deadline,
                                                                               'stage_id': self.stage_id.id,
                                                                               'call_deal_quarter': self.call_deal_quarter,
                                                                               'bu_call_deal_quarter': self.bu_call_deal_quarter,
                                                                               'bu_call_deal': self.bu_call_deal,
                                                                               'ref_id': self.id,
                                                                               })
        if count > 0:
            slipups_log_id = self.env['opportunity.slipups.log'].create({'opportunity_id': self.id,
                                                                         'seller_call_deal': self.seller_call_deal,
                                                                         'zebra_rating': self.zebra_rating,
                                                                         'date_deadline': self.date_deadline,
                                                                         'stage_id': self.stage_id.id,
                                                                         'call_deal_quarter': self.call_deal_quarter,
                                                                         'bu_call_deal_quarter': self.bu_call_deal_quarter,
                                                                         'bu_call_deal': self.bu_call_deal,
                                                                         'ref_id': self.id,
                                                                         })
        return crm_id

    @api.model
    def checking_opportunity_active_pipe(self):
        crmLeadObj = self.env['crm.lead']
        case_stageObj = self.env['crm.case.stage']
        res_partnerObj = self.env['res.partner']
        calendar_eventObj = self.env['calendar.event']
        email_logObj = self.env['crm.email.log']
        phone_callObj = self.env['crm.phonecall']
        current_date = datetime.date.today()
        ninety_end_date = datetime.date.today() + timedelta(days=90)
        current_date1 = current_date.strftime('%Y-%m-%d')
        ninety_end_date1 = ninety_end_date.strftime('%Y-%m-%d')

        account_ids = []
        called_deal_ids = []
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])

        lossWinStageBrws = case_stageObj.search(['|', ('probability', '=', 0), ('probability', '=', 100)])
        wlo_stages_list = [stage.id for stage in lossWinStageBrws if stage.type != 'lead']

        stage_list = [stage.id for stage in stage_ids]

        fiscalyear_id = None
        fiscalyear_ids = self.env['account.fiscalyear'].search([('date_start', '<=', current_date),
                                                                ('date_stop', '>=', current_date),
                                                                ('company_id', '=', 4)])
        if fiscalyear_ids:
            fiscalyear_id = fiscalyear_ids[0]
        if fiscalyear_id:

            CrmLeadBrws = crmLeadObj.search([])
            for CrmLeadBrw in CrmLeadBrws:
                # # Current year Active Pipe # #
                if CrmLeadBrw.date_deadline and fiscalyear_id.date_stop >= CrmLeadBrw.date_deadline >= fiscalyear_id.date_start:
                    if CrmLeadBrw.stage_id.id in wlo_stages_list:
                        CrmLeadBrw.wlo_opportunities = True
                    elif CrmLeadBrw.stage_id.id in stage_list:
                        CrmLeadBrw.this_year = True
                else:
                    if CrmLeadBrw.this_year:
                        CrmLeadBrw.this_year = False
                    if CrmLeadBrw.wlo_opportunities:
                        CrmLeadBrw.wlo_opportunities = False

                # # Ninety Days # #
                if CrmLeadBrw.date_deadline and ninety_end_date1 >= CrmLeadBrw.date_deadline >= current_date1:
                    if CrmLeadBrw.stage_id.id in stage_list:
                        CrmLeadBrw.ninety_days = True
                        if CrmLeadBrw.seller_call_deal and CrmLeadBrw.partner_id.id not in called_deal_ids:
                            called_deal_ids.append(CrmLeadBrw.partner_id.id)
                        if CrmLeadBrw.partner_id.id not in account_ids:
                            account_ids.append(CrmLeadBrw.partner_id.id)
                else:
                    if CrmLeadBrw.ninety_days:
                        CrmLeadBrw.ninety_days = False

                # # Called Deals # #
                if CrmLeadBrw.seller_call_deal or CrmLeadBrw.bu_call_deal and CrmLeadBrw.stage_id.id in stage_list:
                    CrmLeadBrw.show_call_deals = True
                    CrmLeadBrw.slippage = False
                else:
                    if fiscalyear_id.date_start <= CrmLeadBrw.date_deadline <= current_date1 and CrmLeadBrw.stage_id.id in stage_list:
                        CrmLeadBrw.slippage = True
                    else:
                        CrmLeadBrw.slippage = False
                    if CrmLeadBrw.show_call_deals:
                        CrmLeadBrw.show_call_deals = False
                if CrmLeadBrw.stage_id.id not in stage_list:
                    CrmLeadBrw.slippage = False

                if CrmLeadBrw.seller_call_deal and not CrmLeadBrw.seller_check:
                    CrmLeadBrw.seller_check = True
                if CrmLeadBrw.bu_call_deal and not CrmLeadBrw.bu_check:
                    CrmLeadBrw.bu_check = True

        self._cr.execute(""" UPDATE res_partner SET ninety_days = False
                               """)
        for account_id in res_partnerObj.search([('id', 'in', account_ids)]):
            account_id.ninety_days = True
            phone_call_id = phone_callObj.search([('parent_id', '=', account_id.id)])
            if phone_call_id:
                account_id.last_phone_date = phone_call_id[0].date

            email_id = email_logObj.search([('parent_id', '=', account_id.id)])
            if email_id:
                account_id.last_email_date = email_id[0].date

            meeting_id = calendar_eventObj.search([('account_id', '=', account_id.id)])
            if meeting_id:
                account_id.last_meeting_date = meeting_id[0].meeting_date

        # Account Activity #
        phone_callBrws = phone_callObj.search([])
        for record in phone_callBrws:
            if record.parent_id and record.parent_id.id in account_ids:
                record.ninety_days = True
            elif record.parent_id and record.parent_id.id not in account_ids:
                if record.ninety_days:
                    record.ninety_days = False
            else:
                pass
        email_logBrws = email_logObj.search([])
        for record in email_logBrws:
            if record.parent_id and record.parent_id.id in account_ids:
                record.ninety_days = True
            elif record.parent_id and record.parent_id.id not in account_ids:
                if record.ninety_days:
                    record.ninety_days = False
            else:
                pass
        calendar_eventBrws = calendar_eventObj.search([])
        for record in calendar_eventBrws:
            if record.account_id and record.account_id.id in account_ids:
                record.ninety_days = True
            elif record.account_id and record.account_id.id not in account_ids:
                if record.ninety_days:
                    record.ninety_days = False
            else:
                pass


class calendar_event(models.Model):
    _inherit = 'calendar.event'

    ninety_days = fields.Boolean('Is in coming 90 days?', readonly=False)


class crm_email_log(models.Model):
    _inherit = 'crm.email.log'

    ninety_days = fields.Boolean('Is in coming 90 days?', readonly=False)


class crm_phonecall(models.Model):
    _inherit = 'crm.phonecall'

    ninety_days = fields.Boolean('Is in coming 90 days?', readonly=False)


class res_partner(models.Model):
    _inherit = 'res.partner'

    ninety_days = fields.Boolean('Is in coming 90 days?', readonly=True)
    last_meeting_date = fields.Date('Last Meeting Date', readonly=True)
    last_email_date = fields.Date('Last Email Date', readonly=True)
    last_phone_date = fields.Date('Last Phone Date', readonly=True)
    called_deal = fields.Date('Called Deal', readonly=True)




