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
import datetime
from datetime import timedelta
import calendar


class stage_wise_closures(models.Model):
    _name = 'stage.wise.closures'
    _description = 'Stage Wise Closures'
    _order = "id desc"

    state_id = fields.Many2one('crm.case.stage', 'Stages', readonly=True)
    user_id = fields.Many2one('res.users', 'Field Salesperson', readonly=True)
    previous_quarter = fields.Float('Previous Quarter', readonly=True)
    current_quarter = fields.Float('Current Quarter', readonly=True)
    next_quarter = fields.Float('Next Quarter', readonly=True)
    next_next_quarter = fields.Float('Next to Next Quarter', readonly=True)
    total = fields.Float('Total', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class closures_weekly_backup(models.Model):
    _name = 'closures.weekly.backup'
    _description = 'Closures Weekly Backup'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead Id', readonly=True)
    user_id = fields.Many2one('res.users', 'Field Salesperson', readonly=True)
    zebra_rating = fields.Float('Zebra Score', readonly=True)
    stage_id = fields.Many2one('crm.case.stage', readonly=True)
    date_deadline = fields.Date('Expected closing date', readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', readonly=True)
    weekly_status = fields.Boolean('Last Week')
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class top_pipe_leads(models.Model):
    _name = 'top.pipe.leads'
    _description = 'Top of the Pipe (Leads)'
    _order = "id desc"

    category = fields.Char('Category', readonly=True)
    last_week_count = fields.Integer('YTD Lest Week Count', readonly=True)
    current_week_count = fields.Integer('Current Week Count', readonly=True)
    change_delta = fields.Char('Change/Delta', readonly=True)
    create_date = fields.Date('Create Date', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class mid_pipe_opportunities(models.Model):
    _name = 'mid.pipe.opportunities'
    _description = 'Mid of the Pipe (Opportunities)'
    _order = "id desc"

    category = fields.Char('Category', readonly=True)
    last_week_count = fields.Integer('YTD Lest Week Count', readonly=True)
    current_week_count = fields.Integer('Current Week Count', readonly=True)
    change_delta = fields.Char('Change/Delta', readonly=True)
    create_date = fields.Date('Create Date', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class bottom_pipe_won(models.Model):
    _name = 'bottom.pipe.won'
    _description = 'Bottom of the Pipe (Won)'
    _order = "id desc"

    category = fields.Char('Category', readonly=True)
    last_week_count = fields.Integer('YTD Lest Week Count', readonly=True)
    current_week_count = fields.Integer('Current Week Count', readonly=True)
    change_delta = fields.Char('Change/Delta', readonly=True)
    create_date = fields.Date('Create Date', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class closures_comparing_backup(models.Model):
    _name = 'closures.comparing.backup'
    _description = 'Closures Comparing Backup'
    _order = "id desc"

    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_revenue = fields.Float('Opportunity Revenue', readonly=True)
    lead_count = fields.Integer('Opportunity Count', readonly=True)
    zebrascore_increased = fields.Integer('Zebra Score Increased Count', readonly=True)
    zebrascore_decreased = fields.Integer('Zebra Score Decreased Count', readonly=True)
    salestage_movedup = fields.Integer('Moved up Sales Stage', readonly=True)
    salestage_moveddown = fields.Integer('Moved Down Sales Stage', readonly=True)
    moved_hold = fields.Integer('Moved to on Hold', readonly=True)
    moved_won = fields.Integer('Moved to Won', readonly=True)
    moved_lost = fields.Integer('Moved to Lost', readonly=True)
    new_addition = fields.Integer('New addition', readonly=True)
    lead_fqo = fields.Integer('Leads FQO', readonly=True)
    lead_veryhot = fields.Integer('Leads Very Hot', readonly=True)
    lead_hot = fields.Integer('Leads Hot', readonly=True)
    lead_warm = fields.Integer('Leads Warm', readonly=True)
    lead_cold = fields.Integer('Leads Cold', readonly=True)
    opp_fqo = fields.Integer('Opportunities FQO', readonly=True)
    opp_veryhot = fields.Integer('Opportunities Very Hot', readonly=True)
    opp_hot = fields.Integer('Opportunities Hot', readonly=True)
    opp_warm = fields.Integer('Opportunities Warm', readonly=True)
    opp_cold = fields.Integer('Opportunities Cold', readonly=True)
    user_id = fields.Many2one('res.users', 'Field Salesperson', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_team_closures(models.Model):
    _name = 'crm.team.closures'
    _description = 'CRM Team Closures'
    _order = "id desc"

    state_id = fields.Many2one('crm.case.stage', 'Stages', readonly=True)
    previous_quarter = fields.Float('Previous Quarter', readonly=True)
    current_quarter = fields.Float('Current Quarter', readonly=True)
    next_quarter = fields.Float('Next Quarter', readonly=True)
    next_next_quarter = fields.Float('Next to Next Quarter', readonly=True)
    total = fields.Float('Total', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_committed_closures_previous(models.Model):
    _name = 'crm.committed.closures.previous'
    _description = 'Crm Committed Closures Previous'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id",
                                 store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True,
                                  readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    department_product_ids = fields.Many2many('department.product', 'closures_previous_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_committed_closures_current(models.Model):
    _name = 'crm.committed.closures.current'
    _description = 'Crm Committed Closures Current'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id",
                                 store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True,
                                  readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    department_product_ids = fields.Many2many('department.product', 'closures_current_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_committed_closures_next(models.Model):
    _name = 'crm.committed.closures.next'
    _description = 'Crm Committed Closures Next'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id",
                                 store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True,
                                  readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    department_product_ids = fields.Many2many('department.product', 'closures_next_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_committed_closures_next_tonext(models.Model):
    _name = 'crm.committed.closures.next.tonext'
    _description = 'Crm Committed Closures Next to Next'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id",
                                 store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True,
                                  readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    department_product_ids = fields.Many2many('department.product', 'closures_tonext_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('crm.committed.closures', 'Reference', readonly=True)


class crm_committed_closures(models.Model):
    _name = 'crm.committed.closures'
    _inherit = ['mail.thread']
    _description = 'CRM Committed Closures'
    _order = "id desc"
    _rec_name = "sales_user"

    sales_user = fields.Many2one('res.users', 'Sales Person', readonly=True, required=True)
    user_id = fields.Many2one('res.users', 'Created User', default=lambda self: self.env.user, readonly=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)
    previous_quarter = fields.Float('Previous Quarter Active Pipeline', readonly=True)
    current_quarter = fields.Float('Current Quarter Active Pipeline', readonly=True)
    next_quarter = fields.Float('Next Quarter Active Pipeline', readonly=True)
    next_next_quarter = fields.Float('Next to Next Quarter Active Pipeline', readonly=True)
    previous_quarter_label = fields.Char('Previous Quarter Active Pipeline', readonly=True)
    current_quarter_label = fields.Char('Current Quarter Active Pipeline', readonly=True)
    next_quarter_label = fields.Char('Next Quarter Active Pipeline', readonly=True)
    next_next_quarter_label = fields.Char('Next to Next Quarter Active Pipeline', readonly=True)
    team_previous_quarter = fields.Float('Team Previous Quarter Active Pipeline', readonly=True)
    team_current_quarter = fields.Float('Team Current Quarter Active Pipeline', readonly=True)
    team_next_quarter = fields.Float('Team Next Quarter Active Pipeline', readonly=True)
    team_next_next_quarter = fields.Float('Team Next to Next Quarter Active Pipeline', readonly=True)
    check_team = fields.Boolean('Check Team', readonly=True, invisble=True)
    top_pip_lead_ids = fields.One2many('top.pipe.leads', 'ref_id', 'Top of the Pipe (Leads)', readonly=True)
    mid_pip_opportunities_ids = fields.One2many('mid.pipe.opportunities', 'ref_id', 'Mid of the Pipe (Opportunities)',
                                                readonly=True)
    bottom_pipe_won_ids = fields.One2many('bottom.pipe.won', 'ref_id', 'Bottom of the Pipe (Won)', readonly=True)
    stage_closures_ids = fields.One2many('stage.wise.closures', 'ref_id', 'Stage Wise Closures', readonly=True)
    team_closures_ids = fields.One2many('crm.team.closures', 'ref_id', 'Team Closures', readonly=True)
    previous_closures_ids = fields.One2many('crm.committed.closures.previous', 'ref_id', 'Previous Closures IDs', readonly=True)
    current_closures_ids = fields.One2many('crm.committed.closures.current', 'ref_id', 'Current Closures IDs', readonly=True)
    next_closures_ids = fields.One2many('crm.committed.closures.next', 'ref_id', 'Next Closures IDs', readonly=True)
    next_tonext_closures_ids = fields.One2many('crm.committed.closures.next.tonext', 'ref_id', 'Next to Next Closures IDs', readonly=True)
    date = fields.Date('Date', readonly=True, default=lambda self: fields.datetime.now())
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env['res.company']._company_default_get('crm_committed_closures'))

    _sql_constraints = {('sales_user_uniq', 'unique(sales_user)', ' For this user already committed closure created.')}

    @api.model
    def committed_closures(self):
        month = datetime.date.today().month
        year = datetime.date.today().year
        q1 = [4, 5, 6]
        q2 = [7, 8, 9]
        q3 = [10, 11, 12]
        q4 = [1, 2, 3]

        if month in q1:
            previous_start_date = str(year) + '_' + '01_01'
            previous_end_date = str(year) + '_' + '03_31'
            start_date = str(year) + '_' + '04_01'
            end_date = str(year) + '_' + '06_30'
            next_start_date = str(year) + '_' + '07_01'
            next_end_date = str(year) + '_' + '09_30'
            next_next_start_date = str(year) + '_' + '10_01'
            next_next_end_date = str(year) + '_' + '12_31'
            out_year = ','.join(str(year)).split(',')
            label_current_year = str(out_year[2]) + str(int(out_year[3]) - 1) + '-' + str(out_year[2]) + str(out_year[3])
            label_next_year = str(out_year[2]) + str(out_year[3]) + '-' + str(out_year[2]) + str(int(out_year[3]) + 1)
            previous_quarter_label = 'Q4 FY' + label_current_year + '( Jan, Feb, March -' + str(year) + ')'
            current_quarter_label = 'Q1 FY:' + label_next_year + '( April, May, June - ' + str(year) + ')'
            next_quarter_label = 'Q2 FY:' + label_next_year + '( July, August, Sept - ' + str(year) + ')'
            next_next_quarter_label = 'Q3 FY:' + label_next_year + '( Oct, Nov, Dec - ' + str(year) + ')'
        elif month in q2:
            previous_start_date = str(year) + '_' + '04_01'
            previous_end_date = str(year) + '_' + '06_30'
            start_date = str(year) + '_' + '07_01'
            end_date = str(year) + '_' + '09_30'
            next_start_date = str(year) + '_' + '10_01'
            next_end_date = str(year) + '_' + '12_31'
            next_year = year + 1
            next_next_start_date = str(next_year) + '_' + '01_01'
            next_next_end_date = str(next_year) + '_' + '03_31'
            out_year = ','.join(str(year)).split(',')
            label_current_year = str(out_year[2]) + str(out_year[3]) + '-' + str(out_year[2]) + str(int(out_year[3]) + 1)
            previous_quarter_label = 'Q1 FY' + label_current_year + '( April, May, June - ' + str(year) + ')'
            current_quarter_label = 'Q2 FY:' + label_current_year + '( July, August, Sept - ' + str(year) + ')'
            next_quarter_label = 'Q3 FY:' + label_current_year + '( Oct, Nov, Dec - ' + str(year) + ')'
            next_next_quarter_label = 'Q4 FY:' + label_current_year + '( Jan, Feb, March -' + str(year + 1) + ')'
        elif month in q3:
            previous_start_date = str(year) + '_' + '07_01'
            previous_end_date = str(year) + '_' + '09_30'
            start_date = str(year) + '_' + '10_01'
            end_date = str(year) + '_' + '12_31'
            next_year = year + 1
            next_start_date = str(next_year) + '_' + '01_01'
            next_end_date = str(next_year) + '_' + '03_31'
            next_next_start_date = str(next_year) + '_' + '04_01'
            next_next_end_date = str(next_year) + '_' + '06_30'
            out_year = ','.join(str(year)).split(',')
            label_current_year = str(out_year[2]) + str(out_year[3]) + '-' + str(out_year[2]) + str(int(out_year[3]) + 1)
            label_next_year = str(out_year[2]) + str(int(out_year[3]) + 1) + '-' + str(out_year[2]) + str(int(out_year[3]) + 2)
            previous_quarter_label = 'Q2 FY' + label_current_year + '( July, August, Sept - ' + str(year) + ')'
            current_quarter_label = 'Q3 FY:' + label_current_year + '( Oct, Nov, Dec - ' + str(year) + ')'
            next_quarter_label = 'Q4 FY:' + label_current_year + '( Jan, Feb, March -' + str(year + 1) + ')'
            next_next_quarter_label = 'Q1 FY:' + label_next_year + '( April, May, June - ' + str(year + 1) + ')'
        else:
            previous_year = year - 1
            previous_start_date = str(previous_year) + '_' + '10_01'
            previous_end_date = str(previous_year) + '_' + '12_31'
            start_date = str(year) + '_' + '01_01'
            end_date = str(year) + '_' + '03_31'
            next_start_date = str(year) + '_' + '04_01'
            next_end_date = str(year) + '_' + '06_30'
            next_next_start_date = str(year) + '_' + '07_01'
            next_next_end_date = str(year) + '_' + '09_30'
            out_year = ','.join(str(year)).split(',')
            label_next_year = str(out_year[2]) + str(out_year[3]) + '-' + str(out_year[2]) + str(int(out_year[3]) + 1)
            label_current_year = str(out_year[2]) + str(int(out_year[3]) - 1) + '-' + str(out_year[2]) + str(out_year[3])
            previous_quarter_label = 'Q3 FY' + label_current_year + '( Oct, Nov, Dec - ' + str(year - 1) + ')'
            current_quarter_label = 'Q4 FY:' + label_current_year + '( Jan, Feb, March -' + str(year) + ')'
            next_quarter_label = 'Q1 FY:' + label_next_year + '( April, May, June - ' + str(year) + ')'
            next_next_quarter_label = 'Q2 FY:' + label_next_year + '( July, August, Sept - ' + str(year) + ')'

        crmLeadObj = self.env['crm.lead']
        closures_previousObj = self.env['crm.committed.closures.previous']
        closures_currentObj = self.env['crm.committed.closures.current']
        closures_nextObj = self.env['crm.committed.closures.next']
        closures_next_tonextObj = self.env['crm.committed.closures.next.tonext']
        stage_closuresObj = self.env['stage.wise.closures']
        team_closuresObj = self.env['crm.team.closures']
        manager_relationObj = self.env['manager.users.relation']
        selfObj = self.env['crm.committed.closures']
        saleperson_targetObj = self.env['saleperson.target']
        case_stageObj = self.env['crm.case.stage']
        lead_deltaObj = self.env['crm.lead.delta']
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])

        fields_user_ids = self.env['crm.users.mapping'].search([('sales_category', '=', 'FieldSales'),
                                                                ('state', '!=', 'draft')])
        state_ids = []
        if stage_ids:
            for state in stage_ids:
                state_ids.append(state.id)
        for fields_user in fields_user_ids:
            previous_quarter_lead_ids = []
            current_quarter_lead_ids = []
            next_quarter_lead_ids = []
            next_next_quarter_lead_ids = []
            committed_closures = selfObj.search([('sales_user', '=', fields_user.user_id.id)])
            saleperson_target_id = saleperson_targetObj.search([('user_id', '=', fields_user.user_id.id)])
            sales_target_ids = [sales_person.id for sales_person in saleperson_target_id]
            if len(sales_target_ids) > 1:
                saleperson_target_id = saleperson_target_id[0]
            if committed_closures:
                user_id = committed_closures.sales_user.id
            else:
                committed_closures = selfObj.create({'sales_user': fields_user.user_id.id})
                user_id = committed_closures.sales_user.id
            if saleperson_target_id.manager_user_relation_id.user_id:
                committed_closures.sales_manager = saleperson_target_id.manager_user_relation_id.user_id.id
            for state in state_ids:
                previous_quarter = 0.0
                current_quarter = 0.0
                next_quarter = 0.0
                next_next_quarter = 0.0
                fields_sales = []
                sales_person_ids = manager_relationObj.search([('user_id', '=', user_id)])
                if sales_person_ids:
                    for sales_person in sales_person_ids[0].fields_sales_ids:
                        fields_sales.append(sales_person.id)
                else:
                    fields_sales.append(fields_user.user_id.id)
                for sales_person in fields_sales:
                    state_previous = 0.0
                    state_current = 0.0
                    state_next = 0.0
                    state_next_next = 0.0
                    for record in crmLeadObj.search([('user_id', '=', sales_person), ('date_deadline', '>=', previous_start_date),
                                                     ('date_deadline', '<=', previous_end_date), ('stage_id', '=', state)]):
                        state_previous += record.planned_revenue
                        if user_id == sales_person:
                            previous_quarter_lead_ids.append(record.id)
                            delta_closures_previous = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                            difference = 0
                            if delta_closures_previous:
                                if delta_closures_previous[0].date_deadline:
                                    previous_closures_date = datetime.datetime.strptime(delta_closures_previous[0].date_deadline, "%Y-%m-%d")
                                    updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                                    difference = int((updated_closures_date - previous_closures_date).days)
                                    if not difference > 0:
                                        difference = 0

                            previous_closure = closures_previousObj.search([('lead_id', '=', record.id),
                                                                            ('ref_id', '=', committed_closures.id)])
                            if previous_closure:
                                previous_closure.delay_days = difference
                            else:
                                closures_previousObj.create({'lead_id': record.id,
                                                             'delay_days': difference,
                                                             'ref_id': committed_closures.id,
                                                             })

                    for record in crmLeadObj.search([('user_id', '=', sales_person), ('date_deadline', '>=', start_date),
                                                     ('date_deadline', '<=', end_date), ('stage_id', '=', state)]):
                        state_current += record.planned_revenue
                        if user_id == sales_person:
                            current_quarter_lead_ids.append(record.id)
                            delta_closures_current = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                            difference = 0
                            if delta_closures_current:
                                if delta_closures_current[0].date_deadline:
                                    previous_closures_date = datetime.datetime.strptime(delta_closures_current[0].date_deadline, "%Y-%m-%d")
                                    updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                                    difference = int((updated_closures_date - previous_closures_date).days)
                                    if not difference > 0:
                                        difference = 0
                            current_closure = closures_currentObj.search([('lead_id', '=', record.id),
                                                                          ('ref_id', '=', committed_closures.id)])
                            if current_closure:
                                current_closure.delay_days = difference
                            else:
                                closures_currentObj.create({'lead_id': record.id,
                                                            'delay_days': difference,
                                                            'ref_id': committed_closures.id,
                                                            })

                    for record in crmLeadObj.search([('user_id', '=', sales_person), ('date_deadline', '>=', next_start_date),
                                                     ('date_deadline', '<=', next_end_date), ('stage_id', '=', state)]):
                        state_next += record.planned_revenue
                        if user_id == sales_person:
                            next_quarter_lead_ids.append(record.id)
                            delta_closures_current = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                            difference = 0
                            if delta_closures_current:
                                if delta_closures_current[0].date_deadline:
                                    previous_closures_date = datetime.datetime.strptime(delta_closures_current[0].date_deadline, "%Y-%m-%d")
                                    updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                                    difference = int((updated_closures_date - previous_closures_date).days)
                                    if not difference > 0:
                                        difference = 0
                            next_closure = closures_nextObj.search([('lead_id', '=', record.id),
                                                                    ('ref_id', '=', committed_closures.id)])
                            if next_closure:
                                next_closure.delay_days = difference
                            else:
                                closures_nextObj.create({'lead_id': record.id,
                                                         'delay_days': difference,
                                                         'ref_id': committed_closures.id,
                                                         })

                    for record in crmLeadObj.search([('user_id', '=', sales_person), ('date_deadline', '>=', next_next_start_date),
                                                     ('date_deadline', '<=', next_next_end_date), ('stage_id', '=', state)]):
                        state_next_next += record.planned_revenue
                        if user_id == sales_person:
                            next_next_quarter_lead_ids.append(record.id)
                            delta_closures_next_next = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                            difference = 0
                            if delta_closures_next_next:
                                if delta_closures_next_next[0].date_deadline:
                                    previous_closures_date = datetime.datetime.strptime(delta_closures_next_next[0].date_deadline, "%Y-%m-%d")
                                    updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                                    difference = int((updated_closures_date - previous_closures_date).days)
                                    if not difference > 0:
                                        difference = 0
                            next_next_closure = closures_next_tonextObj.search([('lead_id', '=', record.id),
                                                                                ('ref_id', '=', committed_closures.id)])
                            if next_next_closure:
                                next_next_closure.delay_days = difference
                            else:
                                closures_next_tonextObj.create({'lead_id': record.id,
                                                                'delay_days': difference,
                                                                'ref_id': committed_closures.id,
                                                                })

                    stage_closures_ids = stage_closuresObj.search([('state_id', '=', state), ('ref_id', '=', committed_closures.id)])
                    if user_id == sales_person:
                        if not stage_closures_ids:
                            stage_closuresObj.create({'state_id': state,
                                                      'previous_quarter': state_previous,
                                                      'current_quarter': state_current,
                                                      'next_quarter': state_next,
                                                      'next_next_quarter': state_next_next,
                                                      'ref_id': committed_closures.id,
                                                      })
                        else:
                            stage_closures_ids.state_id = state
                            stage_closures_ids.previous_quarter = state_previous
                            stage_closures_ids.current_quarter = state_current
                            stage_closures_ids.next_quarter = state_next
                            stage_closures_ids.next_next_quarter = state_next_next
                    previous_quarter += state_previous
                    current_quarter += state_current
                    next_quarter += state_next
                    next_next_quarter += state_next_next

                if len(fields_sales) > 1:
                    committed_closures.check_team = True
                    team_closures_ids = team_closuresObj.search([('state_id', '=', state), ('ref_id', '=', committed_closures.id)])
                    if not team_closures_ids:
                        team_closuresObj.create({'state_id': state,
                                                 'previous_quarter': previous_quarter,
                                                 'current_quarter': current_quarter,
                                                 'next_quarter': next_quarter,
                                                 'next_next_quarter': next_next_quarter,
                                                 'ref_id': committed_closures.id,
                                                 })
                    else:
                        team_closures_ids.state_id = state
                        team_closures_ids.previous_quarter = previous_quarter
                        team_closures_ids.current_quarter = current_quarter
                        team_closures_ids.next_quarter = next_quarter
                        team_closures_ids.next_next_quarter = next_next_quarter
                else:
                    committed_closures.check_team = False

                fields_sales[:] = []
            # Unlink process for previous closures #
            closures_previous_ids = [closures_previous.id for closures_previous in closures_previousObj.search([
                ('lead_id', 'in', previous_quarter_lead_ids), ('ref_id', '=', committed_closures.id)])]
            total_closures_previous_ids = [closures_previous.id for closures_previous in closures_previousObj.search([
                ('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_closures_previous_ids) - set(closures_previous_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.committed.closures.previous').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            closures_previous_ids[:] = []
            total_closures_previous_ids[:] = []
            previous_quarter_lead_ids[:] = []

            # Unlink process for current closures #
            closures_current_ids = [closures_current.id for closures_current in closures_currentObj.search([
                ('lead_id', 'in', current_quarter_lead_ids), ('ref_id', '=', committed_closures.id)])]
            total_closures_current_ids = [closures_current.id for closures_current in closures_currentObj.search(
                [('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_closures_current_ids) - set(closures_current_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.committed.closures.current').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            closures_current_ids[:] = []
            total_closures_current_ids[:] = []
            current_quarter_lead_ids[:] = []

            # Unlink process for Next closures #
            closures_next_ids = [closures_next.id for closures_next in closures_nextObj.search([
                ('lead_id', 'in', next_quarter_lead_ids), ('ref_id', '=', committed_closures.id)])]
            total_closures_next_ids = [closures_next.id for closures_next in closures_nextObj.search([
                ('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_closures_next_ids) - set(closures_next_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.committed.closures.next').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            closures_current_ids[:] = []
            total_closures_current_ids[:] = []
            next_quarter_lead_ids[:] = []

            # Unlink process for Next to Next closures #
            closures_next_next_ids = [closures_next_next.id for closures_next_next in closures_next_tonextObj.search([
                ('lead_id', 'in', next_next_quarter_lead_ids), ('ref_id', '=', committed_closures.id)])]
            total_closures_next_next_ids = [closures_next_next.id for closures_next_next in closures_nextObj.search([
                ('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_closures_next_next_ids) - set(closures_next_next_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.committed.closures.next.tonext').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            closures_next_next_ids[:] = []
            total_closures_next_next_ids[:] = []
            next_next_quarter_lead_ids[:] = []

            # Unlink process for stages wise #
            stage_wise_ids = [stage_wise.id for stage_wise in stage_closuresObj.search([
                ('state_id', 'in', state_ids), ('ref_id', '=', committed_closures.id)])]
            total_stage_wise_ids = [stage_wise.id for stage_wise in stage_closuresObj.search([
                ('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_stage_wise_ids) - set(stage_wise_ids))
            for unlink_id in unlink_ids:
                self.pool.get('stage.wise.closures').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            total_stage_wise_ids[:] = []
            stage_wise_ids[:] = []

            # Unlink process for team wise #
            team_wise_closure_ids = [team_wise_closure_id.id for team_wise_closure_id in team_closuresObj.search([
                ('state_id', 'in', state_ids), ('ref_id', '=', committed_closures.id)])]
            total_team_wise_closure_ids = [total_team_wise_closure_id.id for total_team_wise_closure_id in
                                           team_closuresObj.search([('ref_id', '=', committed_closures.id)])]
            unlink_ids = list(set(total_team_wise_closure_ids) - set(team_wise_closure_ids))
            for unlink_id in unlink_ids:
                self.pool.get('crm.team.closures').unlink(self._cr, self._uid, unlink_id, self._context)
            unlink_ids[:] = []
            total_team_wise_closure_ids[:] = []
            team_wise_closure_ids[:] = []

            sub_previous_quarter = 0.0
            sub_current_quarter = 0.0
            sub_next_quarter = 0.0
            sub_next_next_quarter = 0.0
            for state in state_ids:
                for stage_wise in stage_closuresObj.search([('state_id', '=', state), ('ref_id', '=', committed_closures.id)]):
                    sub_previous_quarter += stage_wise.previous_quarter
                    sub_current_quarter += stage_wise.current_quarter
                    sub_next_quarter += stage_wise.next_quarter
                    sub_next_next_quarter += stage_wise.next_next_quarter

            committed_closures.previous_quarter = sub_previous_quarter
            committed_closures.current_quarter = sub_current_quarter
            committed_closures.next_quarter = sub_next_quarter
            committed_closures.next_next_quarter = sub_next_next_quarter

            committed_closures.previous_quarter_label = previous_quarter_label
            committed_closures.current_quarter_label = current_quarter_label
            committed_closures.next_quarter_label = next_quarter_label
            committed_closures.next_next_quarter_label = next_next_quarter_label

    @api.model
    def send_automail(self):
        crmLeadObj = self.env['crm.lead']
        weekly_backupObj = self.env['closures.weekly.backup']
        comparing_backupObj = self.env['closures.comparing.backup']
        selfObj = self.env['crm.committed.closures']
        case_stageObj = self.env['crm.case.stage']
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])
        template_id = self.env['ir.model.data'].get_object_reference('crm_dashboard_jmr',
                                                                     'fieldsales_weekly_email_template')[1]
        state_ids = []
        ctx = dict(self._context)
        if stage_ids:
            for state in stage_ids:
                state_ids.append(state.id)
        current_date = datetime.date.today()
        week_end_date = datetime.date.today()
        month = datetime.date.today().month
        year = datetime.date.today().year
        weekday = calendar.day_name[week_end_date.weekday()]
        week_start_date = datetime.date.today() - timedelta(days=7)
        q1 = [4, 5, 6]
        q2 = [7, 8, 9]
        q3 = [10, 11, 12]
        q4 = [1, 2, 3]

        if weekday == 'Wednesday':
            if month in q1:
                start_date = str(year) + '-' + '04-01'
                end_date = str(year) + '-' + '06-30'
            elif month in q2:
                start_date = str(year) + '-' + '07-01'
                end_date = str(year) + '-' + '09-30'
            elif month in q3:
                start_date = str(year) + '-' + '10-01'
                end_date = str(year) + '-' + '12-31'
            else:
                start_date = str(year) + '-' + '01-01'
                end_date = str(year) + '-' + '03-31'
            for fields_user in selfObj.search([('id', '!=', False)]):
                current_week_opp = crmLeadObj.search([('user_id', '=', fields_user.sales_user.id), ('date_deadline', '>=', start_date),
                                                      ('date_deadline', '<=', end_date), ('stage_id', 'in', state_ids)])

                ctx["to"] = self.sales_user.login or ''
                ctx['current_week_opportunities'] = len(current_week_opp)
                ctx['current_week_opp_revenue'] = 0.0
                ctx['zebra_rating_increased_count'] = 0
                ctx['zebra_rating_decreased_count'] = 0
                ctx['stage_increased_count'] = 0
                ctx['stage_decreased_count'] = 0
                ctx['moved_hold_count'] = 0
                ctx['moved_won_count'] = 0
                ctx['moved_lost_count'] = 0
                ctx['new_leads_count'] = 0
                ctx['last_week_opportunities'] = 0
                ctx['last_week_opp_revenue'] = 0
                ctx['opportunities_remark'] = '-'
                ctx['opp_revenue_remark'] = '-'
                ctx['current_opp_cold'] = 0
                ctx['current_opp_warm'] = 0
                ctx['current_opp_hot'] = 0
                ctx['current_opp_very_hot'] = 0
                ctx['current_opp_fqo'] = 0
                ctx['last_week_opp_cold'] = 0
                ctx['last_week_opp_warm'] = 0
                ctx['last_week_opp_hot'] = 0
                ctx['last_week_opp_very_hot'] = 0
                ctx['last_week_opp_fqo'] = 0
                ctx['opp_cold_remark'] = '-'
                ctx['opp_warm_remark'] = '-'
                ctx['opp_hot_remark'] = '-'
                ctx['opp_very_hot_remark'] = '-'
                ctx['opp_fqo_remark'] = '-'
                ctx['opportunity_list'] = []
                current_week_opp_list = []
                for record in current_week_opp:
                    if record.zebra_rating <= 24.0:
                        ctx['current_opp_cold'] += 1
                    elif 25.0 <= record.zebra_rating <= 29.0:
                        ctx['current_opp_warm'] += 1
                    elif 30.0 <= record.zebra_rating <= 34.0:
                        ctx['current_opp_hot'] += 1
                    elif 35.0 <= record.zebra_rating <= 42.0:
                        ctx['current_opp_very_hot'] += 1
                    elif 43.0 <= record.zebra_rating <= 50.0:
                        ctx['current_opp_fqo'] += 1
                    else:
                        pass
                    backup_records = weekly_backupObj.search([('lead_id', '=', record.id), ('ref_id', '=', fields_user.id)])
                    if backup_records:
                        if record.zebra_rating > backup_records[0].zebra_rating:
                            ctx['zebra_rating_increased_count'] += 1
                        elif record.zebra_rating < backup_records[0].zebra_rating:
                            ctx['zebra_rating_decreased_count'] += 1
                        else:
                            pass
                        if record.stage_id.probability > backup_records[0].stage_id.probability:
                            ctx['stage_increased_count'] += 1
                        elif record.stage_id.probability < backup_records[0].stage_id.probability:
                            ctx['stage_decreased_count'] += 1
                        else:
                            pass
                        if record.stage_id.name == 'On Hold' and not backup_records[0].stage_id.name == 'On Hold':
                            ctx['moved_hold_count'] += 1
                        if record.stage_id.name == 'Won' and not backup_records[0].stage_id.name == 'Won':
                            ctx['moved_won_count'] += 1
                        if record.stage_id.name == 'Lost' and not backup_records[0].stage_id.name == 'Lost':
                            ctx['moved_lost_count'] += 1
                    else:
                        ctx['new_leads_count'] += 1

                    weekly_backupObj.create({
                        'lead_id': record.id,
                        'zebra_rating': record.zebra_rating,
                        'stage_id': record.stage_id.id or False,
                        'date_deadline': record.date_deadline,
                        'planned_revenue': record.planned_revenue,
                        'user_id': record.user_id.id or False,
                        'ref_id': fields_user.id,
                    })
                    current_week_opp_list.append(str(record.id))
                    ctx['current_week_opp_revenue'] += record.planned_revenue
                    record_list = []
                    name = record.name.encode('ascii', 'ignore').decode('ascii')
                    record_list.append(str(name))
                    if record.partner_id:
                        partner_name = record.partner_id.name.encode('ascii', 'ignore').decode('ascii')
                        record_list.append(str(partner_name))
                    if record.department_id:
                        department_name = record.department_id.name.encode('ascii', 'ignore').decode('ascii')
                        record_list.append(str(department_name))
                    product_name = ''
                    for product_area in record.department_product_ids:
                        product_name += product_area.name + ', '
                    product = product_name.encode('ascii', 'ignore').decode('ascii')
                    record_list.append(str(product))
                    record_list.append(str(record.planned_revenue))
                    record_list.append(str(record.date_deadline))
                    record_list.append(str(record.zebra_rating))
                    record_list.append(str(record.stage_id.name))
                    ctx['opportunity_list'].append(record_list)
                comparing_records = comparing_backupObj.search([('ref_id', '=', fields_user.id)])
                if comparing_records:
                    ctx['last_week_opp_cold'] = comparing_records[0].opp_cold or 0
                    ctx['last_week_opp_warm'] = comparing_records[0].opp_warm or 0
                    ctx['last_week_opp_hot'] = comparing_records[0].opp_hot or 0
                    ctx['last_week_opp_very_hot'] = comparing_records[0].opp_veryhot or 0
                    ctx['last_week_opp_fqo'] = comparing_records[0].lead_fqo or 0
                    ctx['last_week_opportunities'] = comparing_records[0].opportunity_count or 0
                    ctx['last_week_opp_revenue'] = comparing_records[0].opp_fqo or 0
                    if ctx['last_week_opportunities'] < len(current_week_opp):
                        ctx['opportunities_remark'] = 'Progress'
                    elif ctx['last_week_opportunities'] > len(current_week_opp):
                        ctx['opportunities_remark'] = 'Regress'
                    else:
                        ctx['opportunities_remark'] = 'Same'
                    if comparing_records[0].opportunity_revenue < ctx['current_week_opp_revenue']:
                        ctx['revenue_remark'] = 'Progress'
                    elif comparing_records[0].opportunity_revenue > ctx['current_week_opp_revenue']:
                        ctx['revenue_remark'] = 'Regress'
                    else:
                        ctx['revenue_remark'] = 'Same'

                # Leads Data #
                current_week_leads = crmLeadObj.search([('user_id', '=', fields_user.sales_user.id), ('create_date', '>=', start_date),
                                                        ('create_date', '<=', end_date), ('type', '=', 'lead')])
                ctx['current_week_leads'] = len(current_week_leads)
                ctx['last_week_leads'] = 0
                ctx['lead_remark'] = '-'
                ctx['lead_revenue_remark'] = '-'
                ctx['current_lead_cold'] = 0
                ctx['current_lead_cold'] = 0
                ctx['current_lead_warm'] = 0
                ctx['current_lead_hot'] = 0
                ctx['current_lead_very_hot'] = 0
                ctx['current_lead_fqo'] = 0
                ctx['last_week_lead_cold'] = 0
                ctx['last_week_lead_warm'] = 0
                ctx['last_week_lead_hot'] = 0
                ctx['last_week_lead_very_hot'] = 0
                ctx['last_week_lead_fqo'] = 0
                ctx['lead_cold_remark'] = '-'
                ctx['lead_warm_remark'] = '-'
                ctx['lead_hot_remark'] = '-'
                ctx['lead_very_hot_remark'] = '-'
                ctx['lead_fqo_remark'] = '-'
                ctx['lead_list'] = []
                for lead in current_week_leads:
                    lead_list = []
                    name = lead.name.encode('ascii', 'ignore').decode('ascii')
                    lead_list.append(str(name))
                    if lead.partner_id:
                        partner_name = lead.partner_id.name.encode('ascii', 'ignore').decode('ascii')
                        lead_list.append(str(partner_name))
                    if lead.department_id:
                        department_name = lead.department_id.name.encode('ascii', 'ignore').decode('ascii')
                        lead_list.append(str(department_name))
                    product_name = ''
                    for product_area in lead.department_product_ids:
                        product_name += product_area.name + ', '
                    product = product_name.encode('ascii', 'ignore').decode('ascii')
                    lead_list.append(str(product))
                    lead_list.append(str(lead.planned_revenue))
                    lead_list.append(str(lead.zebra_rating))
                    lead_list.append(str(lead.stage_id.name))
                    ctx['lead_list'].append(lead_list)
                    if lead.zebra_rating <= 24.0:
                        ctx['current_lead_cold'] += 1
                    elif 25.0 <= lead.zebra_rating <= 29.0:
                        ctx['current_lead_warm'] += 1
                    elif 30.0 <= lead.zebra_rating <= 34.0:
                        ctx['current_lead_hot'] += 1
                    elif 35.0 <= lead.zebra_rating <= 42.0:
                        ctx['current_lead_very_hot'] += 1
                    elif 43.0 <= lead.zebra_rating <= 50.0:
                        ctx['current_lead_fqo'] += 1
                    else:
                        pass
                    backup_lead_records = comparing_backupObj.search([('ref_id', '=', fields_user.id)])
                    if backup_lead_records:
                        ctx['last_week_leads'] = backup_lead_records[0].lead_count or 0
                        ctx['last_week_lead_cold'] = backup_lead_records[0].lead_cold or 0
                        ctx['last_week_lead_warm'] = backup_lead_records[0].lead_warm or 0
                        ctx['last_week_lead_hot'] = backup_lead_records[0].lead_hot or 0
                        ctx['last_week_lead_very_hot'] = backup_lead_records[0].lead_veryhot or 0
                        ctx['current_lead_fqo'] = backup_lead_records[0].lead_fqo or 0

                self.pool.get('email.template').send_mail(self._cr, self._uid, template_id, fields_user.id, force_send=False,
                                                          raise_exception=True, context=ctx)
                self.env['closures.comparing.backup'].create({
                    'opportunity_count': len(current_week_opp),
                    'opportunity_revenue': ctx['current_week_opp_revenue'],
                    'lead_count': len(current_week_leads),
                    'zebrascore_increased': ctx['zebra_rating_increased_count'],
                    'zebrascore_decreased': ctx['zebra_rating_decreased_count'],
                    'salestage_movedup': ctx['stage_increased_count'],
                    'salestage_moveddown': ctx['stage_decreased_count'],
                    'moved_hold': ctx['moved_hold_count'],
                    'moved_won': ctx['moved_won_count'],
                    'moved_lost': ctx['moved_lost_count'],
                    'new_addition': ctx['new_leads_count'],
                    'lead_fqo': ctx['current_lead_fqo'],
                    'lead_veryhot': ctx['current_lead_very_hot'],
                    'lead_hot': ctx['current_lead_hot'],
                    'lead_warm': ctx['current_lead_warm'],
                    'lead_cold': ctx['current_lead_cold'],
                    'opp_fqo': ctx['current_opp_fqo'],
                    'opp_veryhot': ctx['current_opp_very_hot'],
                    'opp_hot': ctx['current_opp_hot'],
                    'opp_warm': ctx['current_opp_warm'],
                    'opp_cold': ctx['current_opp_cold'],
                    'ref_id': fields_user.id,
                })

    @api.model
    def weekly_sales_report_calculation(self):
        selfObj = self.env['crm.committed.closures']
        lead_list = ['FQO ( Zebra 43-50):', 'Very Hot (Zebra 35-42):', 'Hot (Zebra 30-35):',
                     'Warm (Zebra 25-29):', 'Cold ( Zebra 0-25):', 'No. of Leads:']
        opportunities_list = ['FQO ( Zebra 43-50):', 'Very Hot (Zebra 35-42):', 'Hot (Zebra 30-35):',
                              'Warm (Zebra 25-29):', 'Cold ( Zebra 0-25):', 'Value:',  'No. of Opportunities:']
        won_list = ['FQO ( Zebra 43-50):', 'Very Hot (Zebra 35-42):', 'Hot (Zebra 30-35):',
                    'Warm (Zebra 25-29):', 'Cold ( Zebra 0-25):', 'Value:', 'No. of Wins:']
        for fields_user in selfObj.search([('id', '!=', False)]):
            for line in lead_list:
                self.env['top.pipe.leads'].create({'category': line,
                                                   'ref_id': fields_user.id,
                                                   })
            for line in opportunities_list:
                self.env['mid.pipe.opportunities'].create({'category': line,
                                                           'ref_id': fields_user.id,
                                                           })
            for line in won_list:
                self.env['bottom.pipe.won'].create({'category': line,
                                                   'ref_id': fields_user.id,
                                                    })
