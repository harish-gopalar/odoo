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


class bu_stage_wise_closures(models.Model):
    _name = 'bu.stage.wise.closures'
    _description = 'Stage Wise Closures'
    _order = "id desc"

    state_id = fields.Many2one('crm.case.stage', 'Stages', readonly=True)
    user_id = fields.Many2one('res.users', 'Created User', readonly=True)
    previous_quarter = fields.Float('Previous Quarter', readonly=True)
    current_quarter = fields.Float('Current Quarter', readonly=True)
    next_quarter = fields.Float('Next Quarter', readonly=True)
    next_next_quarter = fields.Float('Next to Next Quarter', readonly=True)
    total = fields.Float('Total', readonly=True)
    ref_id = fields.Many2one('bu.crm.committed.closures', 'Reference', readonly=True)


class bu_committed_closures_previous(models.Model):
    _name = 'bu.committed.closures.previous'
    _description = 'BU Committed Closures Previous'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_closures_previous_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    remarks = fields.Text('Remarks')
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('bu.committed.closures', 'Reference', readonly=True)


class bu_committed_closures_current(models.Model):
    _name = 'bu.committed.closures.current'
    _description = 'BU Committed Closures Current'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_closures_current_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    remarks = fields.Text('Remarks')
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('bu.committed.closures', 'Reference', readonly=True)


class bu_committed_closures_next(models.Model):
    _name = 'bu.committed.closures.next'
    _description = 'BU Committed Closures Next'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_closures_next_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    remarks = fields.Text('Remarks')
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('bu.committed.closures', 'Reference', readonly=True)


class bu_committed_closures_next_tonext(models.Model):
    _name = 'bu.committed.closures.next.tonext'
    _description = 'BU Committed Closures Next to Next'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    date_deadline = fields.Date('Expected closing date', related="lead_id.date_deadline", store=True, readonly=True)
    planned_revenue = fields.Float('Expected OrderBooking', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_closures_tonext_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    zebra_rating = fields.Float('Zebra Score', related="lead_id.zebra_rating", store=True, readonly=True)
    state_id = fields.Many2one('crm.case.stage', 'Stages', related="lead_id.stage_id", store=True, readonly=True)
    remarks = fields.Text('Remarks')
    delay_days = fields.Integer('Delay Days', readonly=True)
    ref_id = fields.Many2one('bu.committed.closures', 'Reference', readonly=True)


class bu_committed_closures(models.Model):
    _name = 'bu.committed.closures'
    _inherit = ['mail.thread']
    _description = 'BU Committed Closures'
    _order = "id desc"
    _rec_name = "department_id"

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True, required=True)
    previous_quarter = fields.Float('Previous Quarter Pipeline', readonly=True)
    current_quarter = fields.Float('Current Quarter Pipeline', readonly=True)
    next_quarter = fields.Float('Next Quarter Pipeline', readonly=True)
    next_next_quarter = fields.Float('Next to Next Quarter', readonly=True)
    previous_quarter_label = fields.Char('Previous Quarter', readonly=True)
    current_quarter_label = fields.Char('Current Quarter', readonly=True)
    next_quarter_label = fields.Char('Next Quarter', readonly=True)
    next_next_quarter_label = fields.Char('Next to Next Quarter', readonly=True)
    check_team = fields.Boolean('Check Team', readonly=True, invisble=True)
    bu_stage_closures_ids = fields.One2many('bu.stage.wise.closures', 'ref_id', 'Stage Wise Closures', readonly=True)
    bu_previous_closures_ids = fields.One2many('bu.committed.closures.previous', 'ref_id', 'Previous Closures IDs', readonly=False)
    bu_current_closures_ids = fields.One2many('bu.committed.closures.current', 'ref_id', 'Current Closures IDs', readonly=False)
    bu_next_closures_ids = fields.One2many('bu.committed.closures.next', 'ref_id', 'Next Closures IDs', readonly=False)
    bu_next_tonext_closures_ids = fields.One2many('bu.committed.closures.next.tonext', 'ref_id', 'Next to Next Closures IDs', readonly=False)
    date = fields.Date('Date', readonly=True, default=lambda self: fields.datetime.now())
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 default=lambda self: self.env['res.company']._company_default_get('crm_committed_closures'))

    _sql_constraints = {('department_id_uniq', 'unique(department_id)', ' For this BU already committed closure created.')}

    @api.model
    def bu_committed_closures(self):
        current_date = datetime.date.today().month
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
        closures_previousObj = self.env['bu.committed.closures.previous']
        closures_currentObj = self.env['bu.committed.closures.current']
        closures_nextObj = self.env['bu.committed.closures.next']
        closures_next_tonextObj = self.env['bu.committed.closures.next.tonext']
        stage_closuresObj = self.env['bu.stage.wise.closures']
        selfObj = self.env['bu.committed.closures']
        case_stageObj = self.env['crm.case.stage']
        lead_deltaObj = self.env['crm.lead.delta']
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])

        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        state_ids = []
        if stage_ids:
            for state in stage_ids:
                state_ids.append(state.id)
        bu_closures_ids = []
        for state_closures in stage_closuresObj.search([('state_id', 'in', state_ids)]):
            state_closures.previous_quarter = 0.0
            state_closures.current_quarter = 0.0
            state_closures.next_quarter = 0.0
            state_closures.next_next_quarter = 0.0
        previous_quarter_lead_ids = []
        current_quarter_lead_ids = []
        next_quarter_lead_ids = []
        next_next_quarter_lead_ids = []
        bu_records = []
        for bu in bu_ids:
            previous_quarter = 0.0
            current_quarter = 0.0
            next_quarter = 0.0
            next_next_quarter = 0.0
            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                if bu_child:
                    bu_id = bu_child[0].id
            else:
                bu_id = bu.id
            bu_committed_closures = selfObj.search([('department_id', '=', bu_id)])
            if not bu_committed_closures:
                bu_committed_closures = selfObj.create({'department_id': bu_id})

            bu_closures_ids.append(bu_committed_closures.id)
            bu_records.append(bu_id)
            for state in state_ids:
                state_previous = 0.0
                state_current = 0.0
                state_next = 0.0
                state_next_next = 0.0
                for record in crmLeadObj.search([('department_id', '=', bu.id), ('date_deadline', '>=', previous_start_date),
                                                 ('date_deadline', '<=', previous_end_date), ('stage_id', '=', state)]):
                    state_previous += record.planned_revenue
                    previous_quarter_lead_ids.append(record.id)
                    bu_closures_previous = closures_previousObj.search([('lead_id', '=', record.id),
                                                                        ('ref_id', '=', bu_committed_closures.id)])
                    delta_closures_previous = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                    difference = 0
                    if delta_closures_previous:
                        if delta_closures_previous[0].date_deadline:
                            previous_closures_date = datetime.datetime.strptime(delta_closures_previous[0].date_deadline, "%Y-%m-%d")
                            updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                            difference = int((updated_closures_date - previous_closures_date).days)
                            if not difference > 0:
                                difference = 0
                    if not bu_closures_previous:
                        closures_previousObj.create({'lead_id': record.id,
                                                     'delay_days': difference,
                                                     'ref_id': bu_committed_closures.id,
                                                     })
                    else:
                        if len(bu_closures_previous) > 1:
                            bu_closures_previous[0].delay_days = difference
                        else:
                            bu_closures_previous.delay_days = difference

                for record in crmLeadObj.search([('department_id', '=', bu.id), ('date_deadline', '>=', start_date),
                                                 ('date_deadline', '<=', end_date), ('stage_id', '=', state)]):
                    state_current += record.planned_revenue
                    current_quarter_lead_ids.append(record.id)
                    bu_closures_current = closures_currentObj.search([('lead_id', '=', record.id),
                                                                      ('ref_id', '=', bu_committed_closures.id)])
                    delta_closures_current = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                    difference = 0
                    if delta_closures_current:
                        if delta_closures_current[0].date_deadline:
                            previous_closures_date = datetime.datetime.strptime(delta_closures_current[0].date_deadline, "%Y-%m-%d")
                            updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                            difference = int((updated_closures_date - previous_closures_date).days)
                            if not difference > 0:
                                difference = 0
                    if not bu_closures_current:
                        closures_currentObj.create({'lead_id': record.id,
                                                    'delay_days': difference,
                                                    'ref_id': bu_committed_closures.id,
                                                    })
                    else:
                        bu_closures_current.delay_days = difference
                for record in crmLeadObj.search([('department_id', '=', bu.id), ('date_deadline', '>=', next_start_date),
                                                 ('date_deadline', '<=', next_end_date), ('stage_id', '=', state)]):
                    state_next += record.planned_revenue
                    next_quarter_lead_ids.append(record.id)
                    bu_closures_next = closures_nextObj.search([('lead_id', '=', record.id),
                                                                ('ref_id', '=', bu_committed_closures.id)])
                    delta_closures_next = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                    difference = 0
                    if delta_closures_next:
                        if delta_closures_next[0].date_deadline:
                            previous_closures_date = datetime.datetime.strptime(delta_closures_next[0].date_deadline, "%Y-%m-%d")
                            updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                            difference = int((updated_closures_date - previous_closures_date).days)
                            if not difference > 0:
                                difference = 0
                    if not bu_closures_next:
                        closures_nextObj.create({'lead_id': record.id,
                                                 'delay_days': difference,
                                                 'ref_id': bu_committed_closures.id,
                                                 })
                    else:
                        bu_closures_next.delay_days = difference

                for record in crmLeadObj.search([('department_id', '=', bu.id), ('date_deadline', '>=', next_next_start_date),
                                                 ('date_deadline', '<=', next_next_end_date), ('stage_id', '=', state)]):
                    state_next_next += record.planned_revenue
                    next_next_quarter_lead_ids.append(record.id)
                    bu_closures_tonext = closures_next_tonextObj.search([('lead_id', '=', record.id),
                                                                         ('ref_id', '=', bu_committed_closures.id)])
                    delta_closures_tonext = lead_deltaObj.search([('crm_lead_id', '=', record.id)])
                    difference = 0
                    if delta_closures_tonext:
                        if delta_closures_tonext[0].date_deadline:
                            previous_closures_date = datetime.datetime.strptime(delta_closures_tonext[0].date_deadline, "%Y-%m-%d")
                            updated_closures_date = datetime.datetime.strptime(record.date_deadline, "%Y-%m-%d")
                            difference = int((updated_closures_date - previous_closures_date).days)
                            if not difference > 0:
                                difference = 0
                    if not bu_closures_tonext:
                        closures_next_tonextObj.create({'lead_id': record.id,
                                                        'delay_days': difference,
                                                        'ref_id': bu_committed_closures.id,
                                                        })
                    else:
                        bu_closures_tonext.delay_days = difference

                stage_closures_ids = stage_closuresObj.search([('state_id', '=', state),
                                                               ('ref_id', '=', bu_committed_closures.id)])
                if not stage_closures_ids:
                    stage_closuresObj.create({'state_id': state,
                                              'previous_quarter': state_previous,
                                              'current_quarter': state_current,
                                              'next_quarter': state_next,
                                              'next_next_quarter': state_next_next,
                                              'ref_id': bu_committed_closures.id,
                                              })
                else:
                    stage_closures_ids.state_id = state
                    stage_closures_ids.previous_quarter += state_previous
                    stage_closures_ids.current_quarter += state_current
                    stage_closures_ids.next_quarter += state_next
                    stage_closures_ids.next_next_quarter += state_next_next
                previous_quarter += state_previous
                current_quarter += state_current
                next_quarter += state_next
                next_next_quarter += state_next_next

            sub_previous_quarter = 0.0
            sub_current_quarter = 0.0
            sub_next_quarter = 0.0
            sub_next_next_quarter = 0.0
            for state in state_ids:
                for stage_wise in stage_closuresObj.search([('state_id', '=', state),
                                                            ('ref_id', '=', bu_committed_closures.id)]):
                    sub_previous_quarter += stage_wise.previous_quarter
                    sub_current_quarter += stage_wise.current_quarter
                    sub_next_quarter += stage_wise.next_quarter
                    sub_next_next_quarter += stage_wise.next_next_quarter

            bu_committed_closures.previous_quarter = sub_previous_quarter
            bu_committed_closures.current_quarter = sub_current_quarter
            bu_committed_closures.next_quarter = sub_next_quarter
            bu_committed_closures.next_next_quarter = sub_next_next_quarter

            bu_committed_closures.previous_quarter_label = previous_quarter_label
            bu_committed_closures.current_quarter_label = current_quarter_label
            bu_committed_closures.next_quarter_label = next_quarter_label
            bu_committed_closures.next_next_quarter_label = next_next_quarter_label

        # Unlink process for previous closures #
        closures_previous_ids = [closures_previous.id for closures_previous in closures_previousObj.search([
            ('lead_id', 'in', previous_quarter_lead_ids)])]

        total_closures_previous_ids = [closures_previous.id for closures_previous in closures_previousObj.search([
            ('id', '!=', False)])]

        unlink_ids = list(set(total_closures_previous_ids) - set(closures_previous_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.committed.closures.previous').unlink(self._cr, self._uid, unlink_id, self._context)

        # Unlink process for current closures #
        closures_current_ids = [closures_current.id for closures_current in closures_currentObj.search([
            ('lead_id', 'in', current_quarter_lead_ids)])]

        total_closures_current_ids = [closures_current.id for closures_current in closures_currentObj.search(
            [('id', '!=', False)])]

        unlink_ids = list(set(total_closures_current_ids) - set(closures_current_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.committed.closures.current').unlink(self._cr, self._uid, unlink_id, self._context)

        # Unlink process for Next closures #
        closures_next_ids = [closures_next.id for closures_next in closures_nextObj.search([
            ('lead_id', 'in', next_quarter_lead_ids)])]

        total_closures_next_ids = [closures_next.id for closures_next in closures_nextObj.search([
            ('id', '!=', False)])]

        unlink_ids = list(set(total_closures_next_ids) - set(closures_next_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.committed.closures.next').unlink(self._cr, self._uid, unlink_id, self._context)

        # Unlink process for Next to Next closures #
        closures_next_next_ids = [closures_next_next.id for closures_next_next in closures_next_tonextObj.search([
            ('lead_id', 'in', next_next_quarter_lead_ids)])]

        total_closures_next_next_ids = [closures_next_next.id for closures_next_next in closures_next_tonextObj.search([
            ('id', '!=', False)])]

        unlink_ids = list(set(total_closures_next_next_ids) - set(closures_next_next_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.committed.closures.next.tonext').unlink(self._cr, self._uid, unlink_id, self._context)

        # Unlink process for stages wise #

        stage_wise_ids = [stage_wise.id for stage_wise in stage_closuresObj.search([('state_id', 'in', state_ids),
                                                                                    ('ref_id', '!=', False)])]

        total_stage_wise_ids = [stage_wise.id for stage_wise in stage_closuresObj.search([('id', '!=', False)])]

        unlink_ids = list(set(total_stage_wise_ids) - set(stage_wise_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.stage.wise.closures').unlink(self._cr, self._uid, unlink_id, self._context)


        # Unlink process for BU records #

        bu_ids = [bu_record.id for bu_record in selfObj.search([('department_id', 'in', bu_records)])]

        total_bu_ids = [bu_record.id for bu_record in selfObj.search([('id', '!=', False)])]

        unlink_bu_ids = list(set(total_bu_ids) - set(bu_ids))

        for unlink_id in unlink_bu_ids:
            self.pool.get('bu.committed.closures').unlink(self._cr, self._uid, unlink_id, self._context)
