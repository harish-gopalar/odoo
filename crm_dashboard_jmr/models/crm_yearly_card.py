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


class target_line(models.Model):
    _name = 'target.line'
    _description = 'Target Line'
    _rec_name = 'name'
    _order = 'name'

    @api.one
    @api.depends('quarter_one', 'quarter_two', 'quarter_three', 'quarter_four')
    def _compute_total(self):
        self.total = self.quarter_one + self.quarter_two + self.quarter_three + self.quarter_four

    name = fields.Char('Name', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year', readonly=True)
    quarter_one = fields.Float('Quarter 1', readonly=False)
    quarter_two = fields.Float('Quarter 2', readonly=False)
    quarter_three = fields.Float('Quarter 3', readonly=False)
    quarter_four = fields.Float('Quarter 4', readonly=False)
    ref_id = fields.Many2one('annual.performance.sheet', 'Annual Performance Sheet', readonly=True)
    total = fields.Float('Total', compute='_compute_total', store=True, readonly=True)


class achievement_line(models.Model):
    _name = 'achievement.line'
    _description = 'Achievement Line'
    _rec_name = 'name'
    _order = 'name'

    @api.one
    @api.depends('quarter_one', 'quarter_two', 'quarter_three', 'quarter_four')
    def _compute_total(self):
        self.total = self.quarter_one + self.quarter_two + self.quarter_three + self.quarter_four

    name = fields.Char('Name', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    quarter_one = fields.Float('Quarter 1', readonly=False)
    quarter_two = fields.Float('Quarter 2', readonly=False)
    quarter_three = fields.Float('Quarter 3', readonly=False)
    quarter_four = fields.Float('Quarter 4', readonly=False)
    ref_id = fields.Many2one('annual.performance.sheet', 'Annual Performance Sheet', readonly=True)
    total = fields.Float('Total', compute='_compute_total', store=True, readonly=True)


class department_line(models.Model):
    _name = 'department.line'
    _description = 'Department Line'
    _rec_name = 'department_id'
    _order = 'department_id'

    @api.one
    @api.depends('ob_target', 'ob_achieved', 'revenue_target', 'revenue_achieved')
    def _compute_percentage(self):
        if self.ob_target:
            self.ob_percentage = round(float(self.ob_achieved) * 100 / self.ob_target, 2)
        else:
            self.ob_percentage = 0.0
        if self.revenue_target:
            self.revenue_percentage = round(float(self.revenue_achieved) * 100 / self.revenue_target, 2)
        else:
            self.revenue_percentage = 0

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    ob_target = fields.Float('OB Target', readonly=False)
    ob_achieved = fields.Float('OB Achieved', readonly=False)
    ob_percentage = fields.Float('OB Achieved %', compute='_compute_percentage', store=True, readonly=True)
    revenue_target = fields.Float('Revenue Target', readonly=False)
    revenue_achieved = fields.Float('Revenue Achieved', readonly=False)
    revenue_percentage = fields.Float('Revenue Achieved %', compute='_compute_percentage', store=True, readonly=True)
    ref_id = fields.Many2one('annual.performance.sheet', 'Annual Performance Sheet', readonly=True)


class annual_performance_sheet(models.Model):
    _name = 'annual.performance.sheet'
    _inherit = ['mail.thread']
    _description = 'Annual Performance Sheet'
    _rec_name = 'employee_id'
    _order = 'employee_id'

    employee_id = fields.Many2one('hr.employee', 'Employee Name')
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    identification_id = fields.Char('Employee ID', related="employee_id.identification_id", store=True, readonly=True)
    designation_id = fields.Many2one('hr.designation', 'Primary Role', related="employee_id.designation_id",
                                     store=True, readonly=True)
    parent_id = fields.Many2one('hr.employee', 'Primary Supervisor', related="employee_id.parent_id", store=True,
                                readonly=True)
    second_designation_id = fields.Many2one('hr.designation', 'Second Role')
    second_parent_id = fields.Many2one('hr.employee', 'Second Supervisor')
    target_line = fields.One2many('target.line', 'ref_id', 'Target Line', readonly=False)
    achievement_line = fields.One2many('achievement.line', 'ref_id', 'Achievement Line', readonly=False)
    department_line = fields.One2many('department.line', 'ref_id', 'Department Line', readonly=False)

    @api.model
    def annual_performance_sheet_schedule(self):
        selfObj = self.env['annual.performance.sheet']
        targetObj = self.env['target.line']
        achievementObj = self.env['achievement.line']
        departmentObj = self.env['department.line']
        seller_quarterObj = self.env['seller.quarter.wise']
        pipeline_quarterObj = self.env['seller.opportunity.pipeline.build']
        analytic_accountObj = self.env['account.analytic.account']
        element_list = ['Pipeline Build', 'Order Booking', 'Revenue']
        bu_list = []
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        for bu in bu_ids:
            bu_id = None
            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')])
                if bu_child:
                    bu_id = bu_child[0].id
            else:
                bu_id = bu.id
            bu_list.append(bu_id)
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
        saleperson_target_ids = self.env['saleperson.target'].search([('manager_user_relation_id', '!=', False)])
        for fields_user in saleperson_target_ids:
            employee_id = self.env['hr.employee'].search([('user_id', '=', fields_user.user_id.id)])
            if employee_id:
                employee_sheet_id = selfObj.search([('employee_id', '=', employee_id.id)])
                if not employee_sheet_id:
                    employee_sheet_id = selfObj.create({'employee_id': employee_id.id})
                else:
                    employee_sheet_id.fiscalyear_id = fiscalyear_id.id
            ob_target = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            pipeline_target = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            revenue_target = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            ob_achieved = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            pipeline_achieved = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            revenue_achieved = {'q1': 0.0, 'q2': 0.0, 'q3': 0.0, 'q4': 0.0}
            bu_ob_target = {}
            bu_revenue_target = {}
            bu_ob_achieved = {}
            bu_revenue_achieved = {}

            for contract_id in analytic_accountObj.search([('date_start', '>=', q1_start_date),
                                                           ('date_start', '<=', q1_end_date),
                                                           ('manager_id', '=', fields_user.user_id.id)]):
                ob_achieved['q1'] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_revenue_achieved:
                    bu_revenue_achieved[contract_id.project_id.business_unit_id.id] = 0.0

                if contract_id.project_id.business_unit_id.id not in bu_ob_achieved:
                    bu_ob_achieved[contract_id.project_id.business_unit_id.id] = 0.0
                bu_ob_achieved[contract_id.project_id.business_unit_id.id] += contract_id.user_contract_value

                for invoice_id in contract_id.pre_invoice_line:
                    if invoice_id.state == 'paid':
                        revenue_achieved['q1'] += invoice_id.total_amount
                        bu_revenue_achieved[contract_id.project_id.business_unit_id.id] += invoice_id.total_amount

            for contract_id in analytic_accountObj.search([('date_start', '>=', q2_start_date),
                                                           ('date_start', '<=', q2_end_date),
                                                           ('manager_id', '=', fields_user.user_id.id)]):
                ob_achieved['q2'] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_ob_achieved:
                    bu_ob_achieved[contract_id.project_id.business_unit_id.id] = 0.0
                bu_ob_achieved[contract_id.project_id.business_unit_id.id] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_revenue_achieved:
                    bu_revenue_achieved[contract_id.project_id.business_unit_id.id] = 0.0

                for invoice_id in contract_id.pre_invoice_line:
                    if invoice_id.state == 'paid':
                        revenue_achieved['q2'] += invoice_id.total_amount
                        bu_revenue_achieved[contract_id.project_id.business_unit_id.id] += invoice_id.total_amount

            for contract_id in analytic_accountObj.search([('date_start', '>=', q3_start_date),
                                                           ('date_start', '<=', q3_end_date),
                                                           ('manager_id', '=', fields_user.user_id.id)]):
                ob_achieved['q3'] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_revenue_achieved:
                    bu_revenue_achieved[contract_id.project_id.business_unit_id.id] = 0.0

                if contract_id.project_id.business_unit_id.id not in bu_ob_achieved:
                    bu_ob_achieved[contract_id.project_id.business_unit_id.id] = 0.0
                bu_ob_achieved[contract_id.project_id.business_unit_id.id] += contract_id.user_contract_value

                for invoice_id in contract_id.pre_invoice_line:
                    if invoice_id.state == 'paid':
                        revenue_achieved['q3'] += invoice_id.total_amount
                        bu_revenue_achieved[contract_id.project_id.business_unit_id.id] += invoice_id.total_amount

            for contract_id in analytic_accountObj.search([('date_start', '>=', q4_start_date),
                                                           ('date_start', '<=', q4_end_date),
                                                           ('manager_id', '=', fields_user.user_id.id)]):
                ob_achieved['q4'] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_ob_achieved:
                    bu_ob_achieved[contract_id.project_id.business_unit_id.id] = 0.0
                bu_ob_achieved[contract_id.project_id.business_unit_id.id] += contract_id.user_contract_value

                if contract_id.project_id.business_unit_id.id not in bu_revenue_achieved:
                    bu_revenue_achieved[contract_id.project_id.business_unit_id.id] = 0.0

                for invoice_id in contract_id.pre_invoice_line:
                    if invoice_id.state == 'paid':
                        revenue_achieved['q4'] += invoice_id.total_amount
                        bu_ob_target[contract_id.project_id.business_unit_id.id] += invoice_id.total_amount

            # # # OB and Revenue Targets # # #

            for quarter_one in seller_quarterObj.search([('name', '=', 'Quarter - 1'),
                                                         ('sales_target_user', '=', fields_user.id)]):
                ob_target['q1'] += quarter_one.ob_target
                revenue_target['q1'] += quarter_one.revenue_target

                if quarter_one.department_id.id not in bu_ob_target:
                    bu_ob_target[quarter_one.department_id.id] = 0.0
                bu_ob_target[quarter_one.department_id.id] += quarter_one.ob_target

                if quarter_one.department_id.id not in bu_revenue_target:
                    bu_revenue_target[quarter_one.department_id.id] = 0.0
                bu_revenue_target[quarter_one.department_id.id] += quarter_one.revenue_target

            for quarter_two in seller_quarterObj.search([('name', '=', 'Quarter - 2'),
                                                         ('sales_target_user', '=', fields_user.id)]):
                ob_target['q2'] += quarter_two.ob_target
                revenue_target['q2'] += quarter_two.revenue_target

                if quarter_two.department_id.id not in bu_ob_target:
                    bu_ob_target[quarter_two.department_id.id] = 0.0
                bu_ob_target[quarter_two.department_id.id] += quarter_two.ob_target

                if quarter_two.department_id.id not in bu_revenue_target:
                    bu_revenue_target[quarter_two.department_id.id] = 0.0
                bu_revenue_target[quarter_two.department_id.id] += quarter_two.revenue_target

            for quarter_three in seller_quarterObj.search([('name', '=', 'Quarter - 3'),
                                                         ('sales_target_user', '=', fields_user.id)]):
                ob_target['q3'] += quarter_three.ob_target
                revenue_target['q4'] += quarter_three.revenue_target

                if quarter_three.department_id.id not in bu_ob_target:
                    bu_ob_target[quarter_three.department_id.id] = 0.0
                bu_ob_target[quarter_three.department_id.id] += quarter_three.ob_target

                if quarter_three.department_id.id not in bu_revenue_target:
                    bu_revenue_target[quarter_three.department_id.id] = 0.0
                bu_revenue_target[quarter_three.department_id.id] += quarter_three.revenue_target

            for quarter_four in seller_quarterObj.search([('name', '=', 'Quarter - 4'),
                                                         ('sales_target_user', '=', fields_user.id)]):
                ob_target['q4'] += quarter_four.ob_target
                revenue_target['q4'] += quarter_four.revenue_target

                if quarter_four.department_id.id not in bu_ob_target:
                    bu_ob_target[quarter_four.department_id.id] = 0.0
                bu_ob_target[quarter_four.department_id.id] += quarter_four.ob_target

                if quarter_four.department_id.id not in bu_revenue_target:
                    bu_revenue_target[quarter_four.department_id.id] = 0.0
                bu_revenue_target[quarter_four.department_id.id] += quarter_four.revenue_target

            # # # Pipeline Targets and achievements # # #

            for quarter_one in pipeline_quarterObj.search([('ref_id.name', '=', 'Q1 (AMJ)'),
                                                           ('sales_target_user', '=', fields_user.id)]):
                pipeline_achieved['q1'] += quarter_one.opportunity_value
                pipeline_target['q1'] += quarter_one.pipeline_build_value
            for quarter_one in pipeline_quarterObj.search([('ref_id.name', '=', 'Q2 (JAS)'),
                                                           ('sales_target_user', '=', fields_user.id)]):
                pipeline_achieved['q2'] += quarter_one.opportunity_value
                pipeline_target['q2'] += quarter_one.pipeline_build_value
            for quarter_one in pipeline_quarterObj.search([('ref_id.name', '=', 'Q3 (OND)'),
                                                           ('sales_target_user', '=', fields_user.id)]):
                pipeline_achieved['q3'] += quarter_one.opportunity_value
                pipeline_target['q4'] += quarter_one.pipeline_build_value
            for quarter_one in pipeline_quarterObj.search([('ref_id.name', '=', 'Q4 (JFM)'),
                                                           ('sales_target_user', '=', fields_user.id)]):
                pipeline_achieved['q4'] += quarter_one.opportunity_value
                pipeline_target['q4'] += quarter_one.pipeline_build_value

            for target in element_list:
                target_record = targetObj.search([('ref_id', '=', employee_sheet_id.id),
                                                  ('name', '=', target)])
                if target == 'Order Booking':
                    if not target_record:
                        targetObj.create({'name': target,
                                          'quarter_one': ob_target['q1'],
                                          'quarter_two': ob_target['q2'],
                                          'quarter_three': ob_target['q3'],
                                          'quarter_four': ob_target['q4'],
                                          'ref_id': employee_sheet_id.id,
                                          })
                    else:
                        target_record.quarter_one = ob_target['q1']
                        target_record.quarter_two = ob_target['q2']
                        target_record.quarter_three = ob_target['q3']
                        target_record.quarter_four = ob_target['q4']

                if target == 'Pipeline Build':
                    if not target_record:
                        targetObj.create({'name': target,
                                          'quarter_one': pipeline_target['q1'],
                                          'quarter_two': pipeline_target['q2'],
                                          'quarter_three': pipeline_target['q3'],
                                          'quarter_four': pipeline_target['q4'],
                                          'ref_id': employee_sheet_id.id,
                                          })
                    else:
                        target_record.quarter_one = pipeline_target['q1']
                        target_record.quarter_two = pipeline_target['q2']
                        target_record.quarter_three = pipeline_target['q3']
                        target_record.quarter_four = pipeline_target['q4']
                if target == 'Revenue':
                    if not target_record:
                        targetObj.create({'name': target,
                                          'quarter_one': revenue_target['q1'],
                                          'quarter_two': revenue_target['q2'],
                                          'quarter_three': revenue_target['q3'],
                                          'quarter_four': revenue_target['q4'],
                                          'ref_id': employee_sheet_id.id,
                                          })
                    else:
                        target_record.quarter_one = revenue_target['q1']
                        target_record.quarter_two = revenue_target['q2']
                        target_record.quarter_three = revenue_target['q3']
                        target_record.quarter_four = revenue_target['q4']
            for achievement in element_list:
                achievement_record = achievementObj.search([('ref_id', '=', employee_sheet_id.id),
                                                            ('name', '=', achievement)])
                if achievement == 'Order Booking':
                    if not achievement_record:
                        achievementObj.create({'name': achievement,
                                               'quarter_one': ob_achieved['q1'],
                                               'quarter_two': ob_achieved['q2'],
                                               'quarter_three': ob_achieved['q3'],
                                               'quarter_four': ob_achieved['q4'],
                                               'ref_id': employee_sheet_id.id,
                                               })
                    else:
                        achievement_record.quarter_one = ob_achieved['q1']
                        achievement_record.quarter_two = ob_achieved['q2']
                        achievement_record.quarter_three = ob_achieved['q3']
                        achievement_record.quarter_four = ob_achieved['q4']

                if achievement == 'Pipeline Build':
                    if not achievement_record:
                        achievementObj.create({'name': achievement,
                                               'quarter_one': pipeline_achieved['q1'],
                                               'quarter_two': pipeline_achieved['q2'],
                                               'quarter_three': pipeline_achieved['q3'],
                                               'quarter_four': pipeline_achieved['q4'],
                                               'ref_id': employee_sheet_id.id,
                                               })
                    else:
                        achievement_record.quarter_one = pipeline_achieved['q1']
                        achievement_record.quarter_two = pipeline_achieved['q2']
                        achievement_record.quarter_three = pipeline_achieved['q3']
                        achievement_record.quarter_four = pipeline_achieved['q4']

                if achievement == 'Revenue':
                    if not achievement_record:
                        achievementObj.create({'name': achievement,
                                               'quarter_one': revenue_achieved['q1'],
                                               'quarter_two': revenue_achieved['q2'],
                                               'quarter_three': revenue_achieved['q3'],
                                               'quarter_four': revenue_achieved['q4'],
                                               'ref_id': employee_sheet_id.id,
                                               })
                    else:
                        achievement_record.quarter_one = revenue_achieved['q1']
                        achievement_record.quarter_two = revenue_achieved['q2']
                        achievement_record.quarter_three = revenue_achieved['q3']
                        achievement_record.quarter_four = revenue_achieved['q4']
            for bu in bu_list:
                department_record = departmentObj.search([('ref_id', '=', employee_sheet_id.id),
                                                          ('department_id', '=', bu)])
                if bu not in bu_ob_target:
                    target_ob = 0.0
                else:
                    target_ob = bu_ob_target[bu]

                if bu not in bu_revenue_target:
                    target_revenue = 0.0
                else:
                    target_revenue = bu_revenue_target[bu]

                if bu not in bu_ob_achieved:
                    achieved_ob = 0.0
                else:
                    achieved_ob = bu_ob_achieved[bu]

                if bu not in bu_revenue_achieved:
                    achieved_revenue = 0.0
                else:
                    achieved_revenue = bu_revenue_achieved[bu]

                if not department_record:
                    department_record = departmentObj.create({'department_id': bu,
                                                              'ob_target': target_ob,
                                                              'revenue_target': target_revenue,
                                                              'ob_achieved': achieved_ob,
                                                              'revenue_achieved': achieved_revenue,
                                                              'ref_id': employee_sheet_id.id,
                                                              })
                else:
                    department_record.ob_target = target_ob
                    department_record.revenue_target = target_revenue
                    department_record.ob_achieved = achieved_ob
                    department_record.revenue_achieved = achieved_revenue
