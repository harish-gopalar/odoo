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


class seller_active_pipe_line(models.Model):
    _name = 'seller.active.pipe.line'
    _inherit = ['mail.thread']
    _description = 'Seller Active Pipe Line'
    _rec_name = "name"

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    name = fields.Selection(AVAILABLE_QUARTERS, 'Quarter', readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson')
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Opportunity Value', readonly=True)
    multi_opportunity_count = fields.Integer('Multi BU Opportunity Count', readonly=True)
    multi_opportunity_value = fields.Float('Multi BU Opportunity Value', readonly=True)
    total_count = fields.Integer('Total Count', readonly=True)
    total_Value = fields.Float('Total Value', readonly=True)
    ref_id = fields.Many2one('seller.active.pipe', 'Reference', readonly=True)


class seller_active_pipe(models.Model):
    _name = 'seller.active.pipe'
    _inherit = ['mail.thread']
    _description = 'Seller Active Pipe'
    _rec_name = "user_id"

    user_id = fields.Many2one('res.users', 'Fields SalesPerson', required=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    opportunity_count = fields.Integer('Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Opportunity Value', readonly=True)
    multi_opportunity_count = fields.Integer('Multi BU Opportunity Count', readonly=True)
    multi_opportunity_value = fields.Float('Multi BU Opportunity Value', readonly=True)
    total_count = fields.Integer('Total Count', readonly=True)
    total_Value = fields.Float('Total Value', readonly=True)
    seller_active_pipe_line = fields.One2many('seller.active.pipe.line', 'ref_id', 'Seller Active Pipe Line',
                                              readonly=False)
    notes = fields.Text('Notes')

    @api.model
    def run_seller_active_pipe(self):
        selfObj = self.env['seller.active.pipe']
        crm_leadObj = self.env['crm.lead']
        res_usersObj = self.env['res.users']
        active_pipe_lineObj = self.env['seller.active.pipe.line']
        field_seller_ids = res_usersObj.search([('sales_category', '=', 'FieldSales')])
        for field_user in field_seller_ids:
            total_achieved = 0
            q1_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q2_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q3_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            q4_levels = {'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0}
            opportunity_ids = crm_leadObj.search([('user_id', '=', field_user.id)])
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
            seller_active_pipe_id = selfObj.search([('user_id', '=', field_user.id)])
            if not seller_active_pipe_id:
                seller_active_pipe_id = selfObj.create({'user_id': field_user.id,
                                                        })
            '''for user_id in opportunity_ids:
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
                    pass'''
            seller_active_pipe_id.total_achieved = total_achieved
            q1_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '1'),
                                                                 ('ref_id', '=', seller_active_pipe_id.id)])
            if not q1_active_pipe_line_id:
                q1_active_pipe_line_id = active_pipe_lineObj.create({'name': '1',
                                                                     'opportunity_count': q1_levels['l0'],
                                                                     'opportunity_value': q1_levels['l1'],
                                                                     'multi_opportunity_count': q1_levels['l2'],
                                                                     'multi_opportunity_value': q1_levels['l3'],
                                                                     'ref_id': seller_active_pipe_id.id,
                                                                     })
            q2_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '2'),
                                                                 ('ref_id', '=', seller_active_pipe_id.id)])
            if not q2_active_pipe_line_id:
                q2_active_pipe_line_id = active_pipe_lineObj.create({'name': '2',
                                                                     'opportunity_count': q2_levels['l0'],
                                                                     'opportunity_value': q2_levels['l1'],
                                                                     'multi_opportunity_count': q2_levels['l2'],
                                                                     'multi_opportunity_value': q2_levels['l3'],
                                                                     'ref_id': seller_active_pipe_id.id,
                                                                     })

            q3_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '3'),
                                                                 ('ref_id', '=', seller_active_pipe_id.id)])
            if not q3_active_pipe_line_id:
                q3_active_pipe_line_id = active_pipe_lineObj.create({'name': '3',
                                                                     'opportunity_count': q3_levels['l0'],
                                                                     'opportunity_value': q3_levels['l1'],
                                                                     'multi_opportunity_count': q3_levels['l2'],
                                                                     'multi_opportunity_value': q3_levels['l3'],
                                                                     'ref_id': seller_active_pipe_id.id,
                                                                     })

            q4_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '4'),
                                                                 ('ref_id', '=', seller_active_pipe_id.id)])
            if not q4_active_pipe_line_id:
                q4_active_pipe_line_id = active_pipe_lineObj.create({'name': '4',
                                                                     'opportunity_count': q4_levels['l0'],
                                                                     'opportunity_value': q4_levels['l1'],
                                                                     'multi_opportunity_count': q4_levels['l2'],
                                                                     'multi_opportunity_value': q4_levels['l3'],
                                                                     'ref_id': seller_active_pipe_id.id,
                                                                     })
class bu_active_pipe_line(models.Model):
    _name = 'bu.active.pipe.line'
    _inherit = ['mail.thread']
    _description = 'BU Active Pipe Line'
    _rec_name = "name"

    AVAILABLE_QUARTERS = [
        ('1', 'Q1 (AMJ)'),
        ('2', 'Q2 (JAS)'),
        ('3', 'Q3 (OND)'),
        ('4', 'Q4 (JFM)'),
    ]

    @api.one
    @api.depends('opportunity_count', 'opportunity_value', 'multi_opportunity_count', 'multi_opportunity_value','total_Value')
    def _compute_total(self):
        self.total_count = self.opportunity_count + self.multi_opportunity_count
        self.total_Value = self.opportunity_value + self.multi_opportunity_value

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year')
    name = fields.Selection(AVAILABLE_QUARTERS, 'Quarter', readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson')
    opportunity_count = fields.Integer('Non multi BU Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Non multi BU  Opportunity Value', readonly=True)
    multi_opportunity_count = fields.Integer('Multi BU Opportunity Count', readonly=True)
    multi_opportunity_value = fields.Float('Multi BU Opportunity Value', readonly=True)
    total_count = fields.Integer('Total Count', readonly=True)
    total_Value = fields.Float('Total Value',compute=_compute_total,store=True, readonly=True)
    ref_id = fields.Many2one('bu.active.pipe', readonly=True)

class bu_active_pipe(models.Model):
    _name = 'bu.active.pipe'
    _inherit = ['mail.thread']
    _description = 'BU Active Pipe'
    _rec_name = "department_id"

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear', 'Fiscal Year', readonly=True)
    opportunity_count = fields.Integer('Non multi BU Opportunity Count', readonly=True)
    opportunity_value = fields.Float('Non multi BU Opportunity Value', readonly=True)
    multi_opportunity_count = fields.Integer('Multi BU Opportunity Count', readonly=True)
    multi_opportunity_value = fields.Float('Multi BU Opportunity Value', readonly=True)
    total_count = fields.Integer('Total Count', readonly=True)
    total_Value = fields.Float('Total Value', readonly=True)
    bu_active_pipe_line = fields.One2many('bu.active.pipe.line', 'ref_id', 'Seller Active Pipe Line', readonly=False)
    notes = fields.Text('Notes')

    
    @api.model
    def run_bu_active_pipe(self):
        q1_opp_list = {}
        q2_opp_list = {}
        q3_opp_list = {}
        q4_opp_list = {}
        q1_multi_list = {}
        q2_multi_list = {}
        q3_multi_list = {}
        q4_multi_list = {}
        case_stageObj = self.env['crm.case.stage']
        selfObj = self.env['bu.active.pipe']
        crm_leadObj = self.env['crm.lead']
        res_usersObj = self.env['res.users']
        active_pipe_lineObj = self.env['bu.active.pipe.line']
        bu_list = []
        fiscalyear_id = None
        current_date = datetime.date.today()
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
        stage_list = []
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])
        if stage_ids:
            for stage in stage_ids:
                stage_list.append(stage.id)
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        for bu in bu_ids:
            bu_id = None
            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')
                                                             ])
                if bu_child:
                    bu_id = bu_child[0]
            else:
                bu_id = bu
            bu_list.append(bu_id)
            opportunity_ids = crm_leadObj.search([('department_id', '=', bu.id), ('stage_id', 'in', stage_list),
                                                  ('date_deadline', '>=', fiscalyear_id.date_start),
                                                  ('date_deadline', '<=', fiscalyear_id.date_stop)
                                                  ])
            
            
            for opportunity_id in opportunity_ids:
                if opportunity_id.date_deadline and q1_start_date <= opportunity_id.date_deadline <= q1_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q1_opp_list:
                            q1_opp_list[bu_id] = [0, 0]
                        q1_opp_list[bu_id][0] += 1
                        q1_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id:
                                if bu_line_id.department_id not in q1_multi_list:
                                    q1_multi_list[bu_line_id.department_id] = [0, 0]
                                q1_multi_list[bu_line_id.department_id][0] += 1
                                q1_multi_list[bu_line_id.department_id][1] += bu_line_id.planned_revenue
                              
                if opportunity_id.date_deadline and q2_start_date <= opportunity_id.date_deadline <= q2_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q2_opp_list:
                            q2_opp_list[bu_id] = [0, 0]
                        q2_opp_list[bu_id][0] += 1
                        q2_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id:
                                if bu_line_id.department_id not in q2_multi_list:
                                    q2_multi_list[bu_line_id.department_id] = [0, 0]
                                q2_multi_list[bu_line_id.department_id][0] += 1
                                q2_multi_list[bu_line_id.department_id][1] += bu_line_id.planned_revenue
                         
                if opportunity_id.date_deadline and q3_start_date <= opportunity_id.date_deadline <= q3_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q3_opp_list:
                            q3_opp_list[bu_id] = [0, 0]
                        q3_opp_list[bu_id][0] += 1
                        q3_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id:
                                if bu_line_id.department_id not in q3_multi_list:
                                    q3_multi_list[bu_line_id.department_id] = [0, 0]
                                q3_multi_list[bu_line_id.department_id][0] += 1
                                q3_multi_list[bu_line_id.department_id][1] += bu_line_id.planned_revenue
                                
                if opportunity_id.date_deadline and q4_start_date <= opportunity_id.date_deadline <= q4_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q4_opp_list:
                            q4_opp_list[bu_id] = [0, 0]
                        q4_opp_list[bu_id][0] += 1
                        q4_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id:
                                if bu_line_id.department_id not in q4_multi_list:
                                    q4_multi_list[bu_line_id.department_id] = [0, 0]
                                q4_multi_list[bu_line_id.department_id][0] += 1
                                q4_multi_list[bu_line_id.department_id][1] += bu_line_id.planned_revenue

        for bu_id in bu_list:
            bu_active_pipe_id = selfObj.search([('department_id', '=', bu_id.id),
                                                ('fiscalyear_id', '=', fiscalyear_id.id)])
            
            
            if not bu_active_pipe_id:
                bu_active_pipe_id = selfObj.create({'department_id': bu_id.id,
                                                    'fiscalyear_id': fiscalyear_id.id,
                                                    })
            
            q1_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '1'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q1_opp_list:
                q1_opp_list[bu_id] = [0,0]

            if bu_id not in q1_multi_list:
                q1_multi_list[bu_id] = [0,0]

            if not q1_active_pipe_line_id:
                q1_active_pipe_line_id = active_pipe_lineObj.create({'name': '1',
                                                                     'opportunity_count': q1_opp_list[bu_id][0],
                                                                     'opportunity_value': q1_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q1_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q1_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     'total_count' : (q1_opp_list[bu_id][0] + q1_multi_list[bu_id][0] )
                                                                     })
            else:
                if bu_id in q1_opp_list:
                    q1_active_pipe_line_id.opportunity_count = q1_opp_list[bu_id][0]
                    q1_active_pipe_line_id.opportunity_value = q1_opp_list[bu_id][1]
                if bu_id in q1_multi_list:
                    q1_active_pipe_line_id.multi_opportunity_count = q1_multi_list[bu_id][0]
                    q1_active_pipe_line_id.multi_opportunity_value = q1_multi_list[bu_id][1]
                    q1_active_pipe_line_id.total_count = (q1_opp_list[bu_id][0] + q1_multi_list[bu_id][0] )

            q2_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '2'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q2_opp_list:
                q2_opp_list[bu_id] = [0, 0]

            if bu_id not in q2_multi_list:
                q2_multi_list[bu_id] = [0, 0]

            if not q2_active_pipe_line_id:
                q2_active_pipe_line_id = active_pipe_lineObj.create({'name': '2',
                                                                     'opportunity_count': q2_opp_list[bu_id][0],
                                                                     'opportunity_value': q2_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q2_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q2_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     'total_count' : (q2_opp_list[bu_id][0] + q2_multi_list[bu_id][0] )
                                                                     })
            else:
                if bu_id in q2_opp_list:
                    q2_active_pipe_line_id.opportunity_count = q2_opp_list[bu_id][0]
                    q2_active_pipe_line_id.opportunity_value = q2_opp_list[bu_id][1]
                if bu_id in q2_multi_list:
                    q2_active_pipe_line_id.multi_opportunity_count = q2_multi_list[bu_id][0]
                    q2_active_pipe_line_id.multi_opportunity_value = q2_multi_list[bu_id][1]
                    q2_active_pipe_line_id.total_count = (q2_opp_list[bu_id][0] + q2_multi_list[bu_id][0] )

            q3_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '3'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q3_opp_list:
                q3_opp_list[bu_id] = [0, 0]

            if bu_id not in q3_multi_list:
                q3_multi_list[bu_id] = [0, 0]

            if not q3_active_pipe_line_id:
                q3_active_pipe_line_id = active_pipe_lineObj.create({'name': '3',
                                                                     'opportunity_count': q3_opp_list[bu_id][0],
                                                                     'opportunity_value': q3_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q3_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q3_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     'total_count' : (q3_opp_list[bu_id][0] + q3_multi_list[bu_id][0] )
                                                                     })
            else:
                if bu_id in q3_opp_list:
                    q3_active_pipe_line_id.opportunity_count = q3_opp_list[bu_id][0]
                    q3_active_pipe_line_id.opportunity_value = q3_opp_list[bu_id][1]
                if bu_id in q3_multi_list:
                    q3_active_pipe_line_id.multi_opportunity_count = q3_multi_list[bu_id][0]
                    q3_active_pipe_line_id.multi_opportunity_value = q3_multi_list[bu_id][1]
                    q3_active_pipe_line_id.total_count = (q3_opp_list[bu_id][0] + q3_multi_list[bu_id][0] )
    
            q4_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '4'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q4_opp_list:
                q4_opp_list[bu_id] = [0, 0]
            if bu_id not in q4_multi_list:
                q4_multi_list[bu_id] = [0, 0]
                
              

            if not q4_active_pipe_line_id:
                q4_active_pipe_line_id = active_pipe_lineObj.create({'name': '4',
                                                                     'opportunity_count': q4_opp_list[bu_id][0],
                                                                     'opportunity_value': q4_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q4_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q4_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     'total_count' : (q4_opp_list[bu_id][0] + q4_multi_list[bu_id][0] )
                                                                     })
            else:
                if bu_id in q4_opp_list:
                    q4_active_pipe_line_id.opportunity_count = q4_opp_list[bu_id][0]
                    q4_active_pipe_line_id.opportunity_value = q4_opp_list[bu_id][1]
                if bu_id in q4_multi_list:
                    q4_active_pipe_line_id.multi_opportunity_count = q4_multi_list[bu_id][0]
                    q4_active_pipe_line_id.multi_opportunity_value = q4_multi_list[bu_id][1]
                    q4_active_pipe_line_id.total_count = (q4_opp_list[bu_id][0] + q4_multi_list[bu_id][0])
                    
            #print "what coming in final",bu_active_pipe_id.id,bu_id,q4_multi_list        
            
            bu_active_pipe_id.opportunity_count = q1_opp_list[bu_id][0] + q2_opp_list[bu_id][0] + q3_opp_list[bu_id][0] + q4_opp_list[bu_id][0]
            bu_active_pipe_id.opportunity_value = q1_opp_list[bu_id][1] + q2_opp_list[bu_id][1] + q3_opp_list[bu_id][1] + q4_opp_list[bu_id][1]
            
            #if (bu_id in q1_multi_list) and (bu_id in q2_multi_list) and (bu_id in q3_multi_list) and (bu_id in q4_multi_list):
            
            bu_active_pipe_id.multi_opportunity_count = q1_multi_list[bu_id][0] + q2_multi_list[bu_id][0] + q3_multi_list[bu_id][0] + q4_multi_list[bu_id][0]
            bu_active_pipe_id.multi_opportunity_value = q1_multi_list[bu_id][1] + q2_multi_list[bu_id][1] + q3_multi_list[bu_id][1] + q4_multi_list[bu_id][1]
            
            bu_active_pipe_id.total_count = bu_active_pipe_id.opportunity_count + bu_active_pipe_id.multi_opportunity_count
            bu_active_pipe_id.total_Value = bu_active_pipe_id.opportunity_value + bu_active_pipe_id.multi_opportunity_value
    
    
    
    @api.model
    def run_bu_active_pipe_harish(self):
        q1_opp_list = {}
        q2_opp_list = {}
        q3_opp_list = {}
        q4_opp_list = {}
        q1_multi_list = {}
        q2_multi_list = {}
        q3_multi_list = {}
        q4_multi_list = {}
        case_stageObj = self.env['crm.case.stage']
        selfObj = self.env['bu.active.pipe']
        crm_leadObj = self.env['crm.lead']
        res_usersObj = self.env['res.users']
        active_pipe_lineObj = self.env['bu.active.pipe.line']
        bu_list = []
        fiscalyear_id = None
        current_date = datetime.date.today()
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
        stage_list = []
        stage_ids = case_stageObj.search([('probability', '!=', 0), ('probability', '!=', 100)])
        if stage_ids:
            for stage in stage_ids:
                stage_list.append(stage.id)
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        for bu in bu_ids:
            bu_id = None
            if bu.parent:
                bu_child = self.env['hr.department'].search([('parent_id', '=', bu.id), ('dept_main_category', '=', 'Non Support')
                                                             ])
                if bu_child:
                    bu_id = bu_child[0]
            else:
                bu_id = bu
            bu_list.append(bu_id)
            opportunity_ids = crm_leadObj.search([('department_id', '=', bu.id), ('stage_id', 'in', stage_list),
                                                  ('date_deadline', '>=', fiscalyear_id.date_start),
                                                  ('date_deadline', '<=', fiscalyear_id.date_stop)
                                                  ])
            for opportunity_id in opportunity_ids:
                if opportunity_id.date_deadline and q1_start_date <= opportunity_id.date_deadline <= q1_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q1_opp_list:
                            q1_opp_list[bu_id] = [0, 0]
                        q1_opp_list[bu_id][0] += 1
                        q1_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q1_multi_list:
                                    q1_multi_list[bu_id] = [0, 0]
                                q1_multi_list[bu_id][0] += 1
                                q1_multi_list[bu_id][1] += opportunity_id.planned_revenue
                if opportunity_id.date_deadline and q2_start_date <= opportunity_id.date_deadline <= q2_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q2_opp_list:
                            q2_opp_list[bu_id] = [0, 0]
                        q2_opp_list[bu_id][0] += 1
                        q2_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q2_multi_list:
                                    q2_multi_list[bu_id] = [0, 0]
                                q2_multi_list[bu_id][0] += 1
                                q2_multi_list[bu_id][1] += opportunity_id.planned_revenue
                if opportunity_id.date_deadline and q3_start_date <= opportunity_id.date_deadline <= q3_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q3_opp_list:
                            q3_opp_list[bu_id] = [0, 0]
                        q3_opp_list[bu_id][0] += 1
                        q3_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q3_multi_list:
                                    q3_multi_list[bu_id] = [0, 0]
                                q3_multi_list[bu_id][0] += 1
                                q3_multi_list[bu_id][1] += opportunity_id.planned_revenue
                if opportunity_id.date_deadline and q4_start_date <= opportunity_id.date_deadline <= q4_end_date:
                    if not opportunity_id.multi_dept:
                        if bu_id not in q4_opp_list:
                            q4_opp_list[bu_id] = [0, 0]
                        q4_opp_list[bu_id][0] += 1
                        q4_opp_list[bu_id][1] += opportunity_id.planned_revenue
                    else:
                        for bu_line_id in opportunity_id.revenue_ratio_line:
                            if bu_line_id.department_id.id == bu.id:
                                if bu_id not in q4_multi_list:
                                    q4_multi_list[bu_id] = [0, 0]
                                q4_multi_list[bu_id][0] += 1
                                q4_multi_list[bu_id][1] += opportunity_id.planned_revenue

        for bu_id in bu_list:
            bu_active_pipe_id = selfObj.search([('department_id', '=', bu_id.id),
                                                ('fiscalyear_id', '=', fiscalyear_id.id)])
            if not bu_active_pipe_id:
                bu_active_pipe_id = selfObj.create({'department_id': bu_id.id,
                                                    'fiscalyear_id': fiscalyear_id.id,
                                                    })
            q1_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '1'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q1_opp_list:
                q1_opp_list[bu_id] = [0, 0]

            if bu_id not in q1_multi_list:
                q1_multi_list[bu_id] = [0, 0]

            if not q1_active_pipe_line_id:
                q1_active_pipe_line_id = active_pipe_lineObj.create({'name': '1',
                                                                     'opportunity_count': q1_opp_list[bu_id][0],
                                                                     'opportunity_value': q1_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q1_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q1_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     })
            else:
                q1_active_pipe_line_id.opportunity_count = q1_opp_list[bu_id][0]
                q1_active_pipe_line_id.opportunity_value = q1_opp_list[bu_id][1]
                q1_active_pipe_line_id.multi_opportunity_count = q1_multi_list[bu_id][0]
                q1_active_pipe_line_id.multi_opportunity_value = q1_multi_list[bu_id][1]

            q2_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '2'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            print
            if bu_id not in q2_opp_list:
                q2_opp_list[bu_id] = [0, 0]

            if bu_id not in q2_multi_list:
                q2_multi_list[bu_id] = [0, 0]

            if not q2_active_pipe_line_id:
                q2_active_pipe_line_id = active_pipe_lineObj.create({'name': '2',
                                                                     'opportunity_count': q2_opp_list[bu_id][0],
                                                                     'opportunity_value': q2_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q2_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q2_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     })
            else:
                q2_active_pipe_line_id.opportunity_count = q2_opp_list[bu_id][0]
                q2_active_pipe_line_id.opportunity_value = q2_opp_list[bu_id][1]
                q2_active_pipe_line_id.multi_opportunity_count = q2_multi_list[bu_id][0]
                q2_active_pipe_line_id.multi_opportunity_value = q2_multi_list[bu_id][1]

            q3_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '3'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q3_opp_list:
                q3_opp_list[bu_id] = [0, 0]

            if bu_id not in q3_multi_list:
                q3_multi_list[bu_id] = [0, 0]

            if not q3_active_pipe_line_id:
                q3_active_pipe_line_id = active_pipe_lineObj.create({'name': '3',
                                                                     'opportunity_count': q3_opp_list[bu_id][0],
                                                                     'opportunity_value': q3_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q3_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q3_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     })
            else:
                q3_active_pipe_line_id.opportunity_count = q3_opp_list[bu_id][0]
                q3_active_pipe_line_id.opportunity_value = q3_opp_list[bu_id][1]
                q3_active_pipe_line_id.multi_opportunity_count = q3_multi_list[bu_id][0]
                q3_active_pipe_line_id.multi_opportunity_value = q3_multi_list[bu_id][1]

            q4_active_pipe_line_id = active_pipe_lineObj.search([('name', '=', '4'),
                                                                 ('ref_id', '=', bu_active_pipe_id.id)])
            if bu_id not in q4_opp_list:
                q4_opp_list[bu_id] = [0, 0]

            if bu_id not in q4_multi_list:
                q4_multi_list[bu_id] = [0, 0]

            if not q4_active_pipe_line_id:
                q4_active_pipe_line_id = active_pipe_lineObj.create({'name': '4',
                                                                     'opportunity_count': q4_opp_list[bu_id][0],
                                                                     'opportunity_value': q4_opp_list[bu_id][1],
                                                                     'multi_opportunity_count': q4_multi_list[bu_id][0],
                                                                     'multi_opportunity_value': q4_multi_list[bu_id][1],
                                                                     'fiscalyear_id': fiscalyear_id.id,
                                                                     'ref_id': bu_active_pipe_id.id,
                                                                     })
            else:
                q4_active_pipe_line_id.opportunity_count = q4_opp_list[bu_id][0]
                q4_active_pipe_line_id.opportunity_value = q4_opp_list[bu_id][1]
                q4_active_pipe_line_id.multi_opportunity_count = q4_multi_list[bu_id][0]
                q4_active_pipe_line_id.multi_opportunity_value = q4_multi_list[bu_id][1]

            bu_active_pipe_id.opportunity_count = q1_opp_list[bu_id][0] + q2_opp_list[bu_id][0] + q3_opp_list[bu_id][0] + q4_opp_list[bu_id][0]
            bu_active_pipe_id.opportunity_value = q1_opp_list[bu_id][1] + q2_opp_list[bu_id][1] + q3_opp_list[bu_id][1] + q4_opp_list[bu_id][1]
            bu_active_pipe_id.multi_opportunity_count = q1_multi_list[bu_id][0] + q2_multi_list[bu_id][0] + q3_multi_list[bu_id][0] + q4_multi_list[bu_id][0]
            bu_active_pipe_id.multi_opportunity_value = q1_multi_list[bu_id][1] + q2_multi_list[bu_id][1] + q3_multi_list[bu_id][1] + q4_multi_list[bu_id][1]
            bu_active_pipe_id.total_count = bu_active_pipe_id.opportunity_count + bu_active_pipe_id.multi_opportunity_count
            bu_active_pipe_id.total_Value = bu_active_pipe_id.opportunity_value + bu_active_pipe_id.multi_opportunity_value
        

class hr_department(models.Model):
    _inherit = 'hr.department'

    @api.multi
    def name_get(self):
        if not self._ids:
            return []
        if type(self._ids) == type(1):
            self._ids = [self._ids]
        reads = self.read(['name','parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

