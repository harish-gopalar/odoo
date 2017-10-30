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

AVAILABLE_QUARTERS = [
    ('1', 'Q1 (AMJ)'),
    ('2', 'Q2 (JAS)'),
    ('3', 'Q3 (OND)'),
    ('4', 'Q4 (JFM)'),
]


class review_wizard(models.Model):
    _name = 'review.wizard'
    _description = 'Review Wizard'
    _order = "id desc"

    AVAILABLE_MENUS = [
        ('0', 'Seller Target v/s Achievement (OB & Revenue)'),
        ('1', 'BU Target v/s Achievement (OB & Revenue)'),
        ('2', 'Seller Pipeline Build'),
        ('3', 'BU Pipeline Build'),
        ('4', 'Opportunities - Active pipe 17-18'),
        ('16', 'BU Opportunities - Active pipe 17-18'),
        ('5', '90 Days - Active pipe 17-18'),
        ('6', 'Called Deal'),
        ('7', 'Review Action Points'),
        ('8', 'Slippage'),
        ('9', 'OMM Dashboard'),
        ('10', 'OMM Mismatch'),
        ('11', 'Account Activity'),
        ('12', 'Seller Account Mapping'),
        ('13', 'BU Account Mapping'),
        ('14', 'Principal Touch Point'),
        ('17', 'Principal Contact'),
        ('15', 'Win/Loss/On Hold'),
    ]

    @api.model
    def _get_seller_values(self):
        review_ids = self.search([('id', '!=', False)])
        if len(review_ids) > 1:
            review_ids = review_ids[0]
        return review_ids.sales_target_user.id

    @api.model
    def _get_department_values(self):
        review_ids = self.search([('id', '!=', False)])
        if len(review_ids) > 1:
            review_ids = review_ids[0]
        return review_ids.department_id.id

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person',
                                        default=lambda self: self._get_seller_values())
    country_id = fields.Many2one('res.country', 'Country')
    user_id = fields.Many2one('res.users', 'Field SalesPerson')
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Call Deal Quarter')
    department_id = fields.Many2one('hr.department', 'Business Unit',
                                    default=lambda self: self._get_department_values())
    menu = fields.Selection(AVAILABLE_MENUS, 'Menu')

    @api.multi
    def show_results(self):
        data_pool = self.env['ir.model.data']
        context = self._context
        domain = []
        form_id = False
        tree_id = False
        kanban_id = False
        graph_id = False
        model = False
        name = ''
        crm_leadObj = self.env['crm.lead']
        bu_revenue_lineObj = self.env['crm.lead.revenue.ratio']
        if self.menu == '0':  # Target v/s Achievement (OB & Revenue)
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_order_booking_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_order_booking_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.seller_order_booking_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.seller_order_booking_graph_view").id
            if self.sales_target_user:
                domain.append(('sales_target_user', '=', self.sales_target_user.id), )
            else:
                pass
            model = 'seller.order.booking'
            name = 'Seller OB & Revenue - Target vs Achievement'

        if self.menu == '1':  # BU Target v/s Achievement (OB & Revenue)
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.bu_order_booking_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.bu_order_booking_graph_view").id
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                pass
            model = 'bu.order.booking'
            name = 'BU OB & Revenue - Target vs Achievement'

        if self.menu == '2':  # Seller Pipeline Build
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_graph").id
            if self.sales_target_user:
                domain.append(('sales_target_user', '=', self.sales_target_user.id), )
            else:
                pass
            model = 'seller.opportunity.pipeline.build'
            name = 'Seller Pipeline Build'

        if self.menu == '3':  # BU Pipeline Build
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_graph").id
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                raise exceptions.ValidationError("Please select BU")

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revIds in bu_revenue_ids:
                                    bu_revIds.lead_id.write({'bu_revenue': bu_revIds.planned_revenue,
                                                             'from_gss_menu': True,
                                                             'bu_revenue_for': self.department_id.name})
                        else:
                            leadId.write({'bu_revenue': leadId.planned_revenue,
                                          'from_gss_menu': True,
                                          'bu_revenue_for': self.department_id.name})

            model = 'bu.pipeline.build'
            name = 'BU Pipeline Build'

        if self.menu == '4':  # Opportunities - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            if self.sales_target_user and not self.department_id:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('this_year', '=', True)]
            elif self.department_id and not self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('this_year', '=', True)]
            elif self.department_id and self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('this_year', '=', True),
                           ('user_id', '=', self.sales_target_user.user_id.id)]
            else:
                domain += [('this_year', '=', True)]
            domain += [('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadIds in lead_ids:
                        if leadIds.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name})
                        else:
                            leadIds.write({'bu_revenue': leadIds.planned_revenue,
                                           'from_gss_menu': True,
                                           'bu_revenue_for': self.department_id.name
                                           })

            if not department_id:
                slead_ids = crm_leadObj.search(
                    [('multi_dept', '=', True), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for sl in slead_ids:
                    sall_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', sl.id)])
                    srevSum = 0
                    sbu_revenue_for = ''
                    for sallrevIds in sall_bu_revenue_ids:
                        srevSum = srevSum + sallrevIds.planned_revenue
                        sbu_revenue_for = sbu_revenue_for + "," + sallrevIds.department_id.name
                    sl.write({'bu_revenue': srevSum, 'from_gss_menu': True, 'bu_revenue_for': sbu_revenue_for})

                non_multi_lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', False), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for nml in non_multi_lead_ids:
                    nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                               'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = 'Opportunities - Active pipe'

        if self.menu == '5':  # 90 Days - Active pipe
            # TODO Work here 5,6
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            if self.sales_target_user and not self.department_id:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('ninety_days', '=', True)]
            elif self.department_id and not self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('ninety_days', '=', True)]
            elif self.department_id and self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('ninety_days', '=', True),
                           ('user_id', '=', self.sales_target_user.user_id.id)]
            else:
                domain += [('ninety_days', '=', True)]
            domain += [('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadIds in lead_ids:
                        if leadIds.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name
                                                            })
                        else:
                            leadIds.write({'bu_revenue': leadIds.planned_revenue,
                                           'from_gss_menu': True,
                                           'bu_revenue_for': self.department_id.name
                                           })

            if not department_id:
                lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', True), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for l in lead_ids:
                    all_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', l.id)])
                    revSum = 0
                    bu_revenue_for = ''
                    for allrevIds in all_bu_revenue_ids:
                        revSum = revSum + allrevIds.planned_revenue
                        bu_revenue_for = bu_revenue_for + "," + allrevIds.department_id.name
                    l.write({'bu_revenue': revSum, 'from_gss_menu': True, 'bu_revenue_for': bu_revenue_for})

                non_multi_lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', False), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for nml in non_multi_lead_ids:
                    nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                               'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = '90 Days - Active pipe'

        if self.menu == '6':  # Called Deals
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            if self.sales_target_user and not self.department_id:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('show_call_deals', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),]
                if self.call_deal_quarter:
                    domain += [('call_deal_quarter', '=', self.call_deal_quarter)]
            elif self.department_id and not self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('show_call_deals', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),]
                if self.call_deal_quarter:
                    domain += [('bu_call_deal_quarter', '=', self.call_deal_quarter)]
            elif self.department_id and self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('show_call_deals', '=', True),
                           ('user_id', '=', self.sales_target_user.user_id.id),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),]
                if self.call_deal_quarter:
                    domain += [('call_deal_quarter', '=', self.call_deal_quarter), ('bu_call_deal_quarter', '=', self.call_deal_quarter)]
            else:
                domain += [('show_call_deals', '=', True), ('stage_id.probability', '<', '100'),
                           ('stage_id.probability', '>', '0'), ]
                if self.call_deal_quarter:
                    domain += ['|', ('call_deal_quarter', '=', self.call_deal_quarter), ('bu_call_deal_quarter', '=', self.call_deal_quarter)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name
                                                            })
                        else:
                            leadId.write({'bu_revenue': leadId.planned_revenue,
                                          'from_gss_menu': True,
                                          'bu_revenue_for': self.department_id.name
                                          })
            if not department_id:
                lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', True), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for l in lead_ids:
                    all_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', l.id)])
                    revSum = 0
                    bu_revenue_for = ''
                    for allrevIds in all_bu_revenue_ids:
                        revSum = revSum + allrevIds.planned_revenue
                        bu_revenue_for = bu_revenue_for + "," + allrevIds.department_id.name
                    l.write({'bu_revenue': revSum, 'from_gss_menu': True, 'bu_revenue_for': bu_revenue_for})

                non_multi_lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', False), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for nml in non_multi_lead_ids:
                    nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                               'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = 'Called Deals'

        if self.menu == '7':  # Plan of Action
            tree_id = self.env.ref("crm_dashboard_jmr.view_plan_action_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_plan_action_form").id
            if self.sales_target_user:
                domain.append(('user_id', '=', self.sales_target_user.user_id.id), )
            elif self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                pass
            model = 'plan.action'
            name = 'Plan of Action'

        if self.menu == '8':  # Slippage
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id

            if self.sales_target_user and not self.department_id:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('slippage', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),
                           ('this_year', '=', True)]
            elif self.department_id and not self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),('this_year', '=', True),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('slippage', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0')]
            elif self.department_id and self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('slippage', '=', True),
                           ('user_id', '=', self.sales_target_user.user_id.id), ('this_year', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0')]
            else:
                domain += [('this_year', '=', True), ('slippage', '=', True), ('stage_id.probability', '<', '100'),
                           ('stage_id.probability', '>', '0')]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadIds in lead_ids:
                        if leadIds.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name
                                                            })
                        else:
                            leadIds.write({'bu_revenue': leadIds.planned_revenue,
                                           'from_gss_menu': True,
                                           'bu_revenue_for': self.department_id.name
                                           })

            if not department_id:
                lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', True), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for l in lead_ids:
                    all_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', l.id)])
                    revSum = 0
                    bu_revenue_for = ''
                    for allrevIds in all_bu_revenue_ids:
                        revSum = revSum + allrevIds.planned_revenue
                        bu_revenue_for = bu_revenue_for + "," + allrevIds.department_id.name
                    l.write({'bu_revenue': revSum, 'from_gss_menu': True, 'bu_revenue_for': bu_revenue_for})

                non_multi_lead_ids = crm_leadObj.search(
                    [('multi_dept', '=', False), ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                     ('stage_id.probability', '>', '0')])
                for nml in non_multi_lead_ids:
                    nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                               'bu_revenue_for': nml.department_id.name})
            model = 'crm.lead'
            name = 'Slippage'

        if self.menu == '9':  # OMM Dashboard
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            if self.sales_target_user:
                domain.append(('user_id', '=', self.sales_target_user.user_id.id), )
            elif self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                pass
            model = 'crm.omm'
            name = 'OMM Dashboard'

        if self.menu == '10':  # OMM Mismatch
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_mismatch_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            if self.sales_target_user:
                domain.append(('user_id', '=', self.sales_target_user.user_id.id), )
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            domain.append(('is_omm_mismatch', '=', True))
            model = 'crm.omm'
            name = 'OMM Mismatch'

        if self.menu == '11':  # Account Activity
            tree_id = self.env.ref("crm_dashboard_jmr.view_Account_activity_tree").id
            form_id = self.env.ref("crm_jmr.view_partner_account_form").id
            if self.sales_target_user:
                domain.append(('user_id', '=', self.sales_target_user.user_id.id), )
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            domain.append(('is_company', '=', True), )
            domain.append(('ninety_days', '=', True), )
            model = 'res.partner'
            name = 'Account Activity'

        if self.menu == '12':  # Seller Account Mapping
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_account_mapping_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_account_mapping_form").id
            if self.sales_target_user:
                domain.append(('user_id', '=', self.sales_target_user.user_id.id), )
            else:
                pass
            model = 'seller.account.mapping'
            name = 'Seller Account Mapping'

        if self.menu == '13':  # BU Account Mapping
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_graph").id
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                pass
            model = 'bu.account.mapping'
            name = 'BU Account Mapping'

        if self.menu == '14':  # Principal Touch Point
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_form").id
            if self.sales_target_user:
                domain.append(('organised_by', '=', self.sales_target_user.user_id.id), )
            elif self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                pass
            model = 'principal.touch.point'
            name = 'Principal Touch Point'

        if self.menu == '15':  # Win/Loss/On Hold
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id

            if self.sales_target_user and not self.department_id:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('wlo_opportunities', '=', True)]
            elif self.department_id and not self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('wlo_opportunities', '=', True)]
            elif self.department_id and self.sales_target_user:
                domain += ['|', ('department_id', '=', self.department_id.id),
                           ('multi_department_ids', 'in', [self.department_id.id]), ('wlo_opportunities', '=', True),
                           ('user_id', '=', self.sales_target_user.user_id.id)]
            else:
                domain += [('wlo_opportunities', '=', True)]
            # Update Multi BU Revenue Value

            lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', 'in', ['100', '0'])])
            for nml in lead_ids:
                nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                           'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = 'Win/Loss/On Hold'

        if self.menu == '16':  # Active pipe Summary
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_form").id
            if self.department_id:
                domain.append(('department_id', '=', self.department_id.id), )
            else:
                raise exceptions.ValidationError("Please select BU")

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name
                                                            })
                        else:
                            leadId.write({'bu_revenue': leadId.planned_revenue,
                                          'from_gss_menu': True,
                                          'bu_revenue_for': self.department_id.name
                                          })

            model = 'bu.active.pipe'
            name = 'BU Active Pipe Summary'

        if self.menu == '17':  # Principal Contacts
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_form").id
            model = 'principal.contact'
            name = 'Principal Contact'

        if self.menu:
            return {
                'type': 'ir.actions.act_window',
                'name': name,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': model,
                'domain': domain,
                'views': [(tree_id, 'tree'), (form_id, 'form'), (kanban_id, 'kanban'), (graph_id, 'graph')],
                'target': 'current',
                'context': context,
            }
        else:
            raise exceptions.ValidationError("Please select Menu")


class seller_review_wizard(models.Model):
    _name = 'seller.review.wizard'
    _description = 'Seller Review Wizard'
    _order = "id desc"

    AVAILABLE_MENUS = [
        ('0', 'Seller Target v/s Achievement (OB & Revenue)'),
        ('1', 'Seller Pipeline Build'),
        ('2', 'Opportunities - Active pipe 17-18'),
        ('3', '90 Days - Active pipe 17-18'),
        ('4', 'Called Deal'),
        ('5', 'Review Action Points'),
        ('6', 'Slippage'),
        ('7', 'OMM Dashboard'),
        ('8', 'OMM Mismatch'),
        ('9', 'Account Activity'),
        ('10', 'Seller Account Mapping'),
        ('11', 'Principal Touch Point'),
        ('13', 'Principal Contact'),
        ('12', 'Win/Loss/On Hold'),
    ]

    @api.model
    def _get_seller_values(self):
        user_id = self.env['saleperson.target'].search([('user_id', '=', self._uid)])
        return user_id.id or False

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        group_ids = []
        user_group_id = [group.id for group in self.pool.get('res.users').browse(cr, uid, uid).groups_id]
        _model, group_id1 = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_BU')
        group_ids.append(group_id1)
        _model, group_id2 = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_crm_bdm')
        group_ids.append(group_id2)
        res = super(seller_review_wizard, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
                                                                context=context, toolbar=toolbar, submenu=submenu)
        count = 0
        if view_type == 'form':
            for group_id in group_ids:
                if group_id in user_group_id:
                    count += 1
            if count == 0:
                doc = etree.XML(res['arch'])
                list1 = ['sales_target_user']
                for l in list1:
                    nodes = doc.xpath("//field[@name='%s']" % l)
                    for node in nodes:
                        node.set('readonly', '1')
                        setup_modifiers(node, res['fields'][l])
                res['arch'] = etree.tostring(doc)
        return res

    sales_target_user = fields.Many2one('saleperson.target', 'Sales Person',
                                        default=lambda self: self._get_seller_values())
    country_id = fields.Many2one('res.country', 'Country')
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Call Deal Quarter')
    department_id = fields.Many2one('hr.department', 'Business Unit')
    menu = fields.Selection(AVAILABLE_MENUS, 'Menu')

    @api.multi
    def show_results(self):
        data_pool = self.env['ir.model.data']
        context = self._context
        domain = []
        form_id = False
        tree_id = False
        kanban_id = False
        graph_id = False
        model = False
        name = ''
        crm_leadObj = self.env['crm.lead']
        bu_revenue_lineObj = self.env['crm.lead.revenue.ratio']
        if not self.sales_target_user:
            raise exceptions.ValidationError("Please select seller")
        if self.menu == '0':  # Target v/s Achievement (OB & Revenue)
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_order_booking_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_order_booking_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.seller_order_booking_kanban").id
            domain += [('sales_target_user', '=', self.sales_target_user.id)]
            model = 'seller.order.booking'
            name = 'Seller OB & Revenue - Target vs Achievement'

        if self.menu == '1':  # Seller Pipeline Build
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_opportunity_pipeline_build_form").id
            domain += [('sales_target_user', '=', self.sales_target_user.id)]
            model = 'seller.opportunity.pipeline.build'
            name = 'Seller Pipeline Build'

        if self.menu == '2':  # Opportunities - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('this_year', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            user_id = self.sales_target_user and self.sales_target_user.user_id.id or False
            seller_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', True),
                                                  ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                  ('stage_id.probability', '>', '0')])
            for sl in seller_lead_ids:
                sall_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', sl.id)])
                srevSum = 0
                sbu_revenue_for = ''
                for sallrevIds in sall_bu_revenue_ids:
                    srevSum = srevSum + sallrevIds.planned_revenue
                    sbu_revenue_for = sbu_revenue_for + "," + sallrevIds.department_id.name
                sl.write({'bu_revenue': srevSum, 'from_gss_menu': True, 'bu_revenue_for': sbu_revenue_for})

            non_multi_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', False),
                                                     ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                     ('stage_id.probability', '>', '0')])
            for nml in non_multi_lead_ids:
                nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                           'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = 'Opportunities - Active pipe'

        if self.menu == '3':  # 90 Days - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('ninety_days', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            user_id = self.sales_target_user and self.sales_target_user.user_id.id or False
            seller_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', True),
                                                  ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                  ('stage_id.probability', '>', '0')])
            for sl in seller_lead_ids:
                sall_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', sl.id)])
                srevSum = 0
                sbu_revenue_for = ''
                for sallrevIds in sall_bu_revenue_ids:
                    srevSum = srevSum + sallrevIds.planned_revenue
                    sbu_revenue_for = sbu_revenue_for + "," + sallrevIds.department_id.name
                sl.write({'bu_revenue': srevSum, 'from_gss_menu': True, 'bu_revenue_for': sbu_revenue_for})

            non_multi_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', False),
                                                     ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                     ('stage_id.probability', '>', '0')])
            for nml in non_multi_lead_ids:
                nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                           'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = '90 Days - Active pipe'

        if self.menu == '4':  # Called Deals
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            if self.sales_target_user:
                domain += [('user_id', '=', self.sales_target_user.user_id.id), ('show_call_deals', '=', True),
                           ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'), ]
                if self.call_deal_quarter:
                    domain += [('call_deal_quarter', '=', self.call_deal_quarter)]

            # Update Multi BU Revenue Value
            user_id = self.sales_target_user and self.sales_target_user.user_id.id or False
            seller_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', True),
                                                  ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                  ('stage_id.probability', '>', '0')])
            for sl in seller_lead_ids:
                sall_bu_revenue_ids = bu_revenue_lineObj.search([('lead_id', '=', sl.id)])
                srevSum = 0
                sbu_revenue_for = ''
                for sallrevIds in sall_bu_revenue_ids:
                    srevSum = srevSum + sallrevIds.planned_revenue
                    sbu_revenue_for = sbu_revenue_for + "," + sallrevIds.department_id.name
                sl.write({'bu_revenue': srevSum, 'from_gss_menu': True, 'bu_revenue_for': sbu_revenue_for})

            non_multi_lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('multi_dept', '=', False),
                                                     ('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                                     ('stage_id.probability', '>', '0')])
            for nml in non_multi_lead_ids:
                nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                           'bu_revenue_for': nml.department_id.name})
            model = 'crm.lead'
            name = 'Called Deals'

        if self.menu == '5':  # Plan of Action
            tree_id = self.env.ref("crm_dashboard_jmr.view_plan_action_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_plan_action_form").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id)]
            model = 'plan.action'
            name = 'Plan of Action'

        if self.menu == '6':  # Slippage
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('slippage', '=', True),
                       ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0')]
            model = 'crm.lead'
            name = 'Slippage'

        if self.menu == '7':  # OMM Dashboard
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id)]
            model = 'crm.omm'
            name = 'OMM Dashboard'

        if self.menu == '8':  # OMM Mismatch
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_mismatch_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('is_omm_mismatch', '=', True)]
            model = 'crm.omm'
            name = 'OMM Mismatch'

        if self.menu == '9':  # Account Activity
            tree_id = self.env.ref("crm_dashboard_jmr.view_Account_activity_tree").id
            form_id = self.env.ref("crm_jmr.view_partner_account_form").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('is_company', '=', True),
                       ('ninety_days', '=', True)]
            model = 'res.partner'
            name = 'Account Activity'

        if self.menu == '10':  # Seller Account Mapping
            tree_id = self.env.ref("crm_dashboard_jmr.view_seller_account_mapping_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_seller_account_mapping_form").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id)]
            model = 'seller.account.mapping'
            name = 'Seller Account Mapping'

        if self.menu == '11':  # Principal Touch Point
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_form").id
            domain += [('organised_by', '=', self.sales_target_user.user_id.id)]
            model = 'principal.touch.point'
            name = 'Principal Touch Point'

        if self.menu == '12':  # Win/Loss/On Hold
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += [('user_id', '=', self.sales_target_user.user_id.id), ('wlo_opportunities', '=', True)]
            # Update Multi BU Revenue Value
            user_id = self.sales_target_user and self.sales_target_user.user_id.id or False
            lead_ids = crm_leadObj.search([('user_id', '=', user_id), ('type', '=', 'opportunity'), ('stage_id.probability', 'in', ['100', '0'])])
            for nml in lead_ids:
                nml.write({'bu_revenue': nml.planned_revenue, 'from_gss_menu': True,
                           'bu_revenue_for': nml.department_id.name})

            model = 'crm.lead'
            name = 'Win/Loss/On Hold'

        if self.menu == '13':  # Principal Contacts
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_form").id
            model = 'principal.contact'
            name = 'Principal Contact'

        if self.menu:
            return {
                'type': 'ir.actions.act_window',
                'name': name,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': model,
                'domain': domain,
                'views': [(tree_id, 'tree'), (form_id, 'form'), (kanban_id, 'kanban'), (graph_id, 'graph')],
                'target': 'current',
                'context': context,
            }
        else:
            raise exceptions.ValidationError("Please select Menu")


class bu_review_wizard(models.Model):
    _name = 'bu.review.wizard'
    _description = 'BU Review Wizard'
    _order = "id desc"

    AVAILABLE_MENUS = [
        ('0', 'BU Target v/s Achievement (OB & Revenue)'),
        ('1', 'BU Pipeline Build'),
        ('2', 'Opportunities - Active pipe 17-18'),
        ('13', 'BU Opportunities - Active pipe 17-18'),
        ('3', '90 Days - Active pipe 17-18'),
        ('4', 'Called Deal'),
        ('5', 'Review Action Points'),
        ('6', 'Slippage'),
        ('7', 'OMM Dashboard'),
        ('8', 'OMM Mismatch'),
        ('9', 'Account Activity'),
        ('10', 'BU Account Mapping'),
        ('11', 'Principal Touch Point'),
        ('14', 'Principal Contact'),
        ('12', 'Win/Loss/On Hold'),
    ]

    @api.model
    def _get_department_values(self):
        department_id = self.env['hr.department'].search([('parent', '=', False),
                                                          ('dept_main_category', '=', 'Non Support'),
                                                          ('manager_id.user_id', '=', self._uid)])
        department_id = department_id and department_id[0].id or False
        return department_id

    user_id = fields.Many2one('res.users', 'Login user', default=lambda self: self.env.user)
    country_id = fields.Many2one('res.country', 'Country')
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Call Deal Quarter')
    department_id = fields.Many2one('hr.department', 'Business Unit',
                                    default=lambda self: self._get_department_values())
    menu = fields.Selection(AVAILABLE_MENUS, 'Menu')

    @api.multi
    def show_results(self):
        data_pool = self.env['ir.model.data']
        context = self._context
        domain = []
        form_id = False
        tree_id = False
        kanban_id = False
        graph_id = False
        model = False
        name = ''
        crm_leadObj = self.env['crm.lead']
        bu_revenue_lineObj = self.env['crm.lead.revenue.ratio']
        if not self.department_id:
            raise exceptions.ValidationError("Please select BU")
        if self.menu == '0':  # BU Target v/s Achievement (OB & Revenue)
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.bu_order_booking_kanban").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'bu.order.booking'
            name = 'BU OB & Revenue - Target vs Achievement'

        if self.menu == '1':  # BU Pipeline Build
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_form").id
            domain += [('department_id', '=', self.department_id.id)]
            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadIds in lead_ids:
                        if leadIds.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revIds in bu_revenue_ids:
                                    bu_revIds.lead_id.write({'bu_revenue': bu_revIds.planned_revenue,
                                                             'from_gss_menu': True,
                                                             'bu_revenue_for': self.department_id.name})
                        else:
                            if leadIds.department_id.id == department_id:
                                leadIds.write({'bu_revenue': leadIds.planned_revenue, 'from_gss_menu': True,
                                               'bu_revenue_for': self.department_id.name})

            model = 'bu.pipeline.build'
            name = 'BU Pipeline Build'

        if self.menu == '2':  # Opportunities - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('this_year', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revIds in bu_revenue_ids:
                                    bu_revIds.lead_id.write({'bu_revenue': bu_revIds.planned_revenue,
                                                             'from_gss_menu': True,
                                                             'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = 'Opportunities - Active pipe'

        if self.menu == '3':  # 90 Days - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('ninety_days', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = '90 Days - Active pipe'

        if self.menu == '4':  # Called Deals
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('show_call_deals', '=', True),
                       ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),]
            if self.call_deal_quarter:
                domain += [('bu_call_deal_quarter', '=', self.call_deal_quarter)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            seller_bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if seller_bu_revenue_ids:
                                for bu_revId in seller_bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})
            model = 'crm.lead'
            name = 'Called Deals'

        if self.menu == '5':  # Plan of Action
            tree_id = self.env.ref("crm_dashboard_jmr.view_plan_action_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_plan_action_form").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'plan.action'
            name = 'Plan of Action'

        if self.menu == '6':  # Slippage
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('slippage', '=', True),
                       ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0')]
            model = 'crm.lead'
            name = 'Slippage'

        if self.menu == '7':  # OMM Dashboard
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'crm.omm'
            name = 'OMM Dashboard'

        if self.menu == '8':  # OMM Mismatch
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_mismatch_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('department_id', '=', self.department_id.id), ('is_omm_mismatch', '=', True)]
            name = 'OMM Mismatch'
            model = 'crm.omm'

        if self.menu == '9':  # TODO: Account Activity
            tree_id = self.env.ref("crm_dashboard_jmr.view_Account_activity_tree").id
            form_id = self.env.ref("crm_jmr.view_partner_account_form").id
            domain += [('department_id', '=', self.department_id.id),
                       ('is_company', '=', True), ('ninety_days', '=', True)]
            model = 'res.partner'
            name = 'Account Activity'

        if self.menu == '10':  # BU Account Mapping
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_graph").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'bu.account.mapping'
            name = 'BU Account Mapping'

        if self.menu == '11':  # Principal Touch Point
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_form").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'principal.touch.point'
            name = 'Principal Touch Point'

        if self.menu == '12':  # Win/Loss/On Hold
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id

            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('wlo_opportunities', '=', True)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search(['|', ('department_id', '=', self.department_id.id),
                                               ('multi_department_ids', 'in', [self.department_id.id]),
                                               ('type', '=', 'opportunity'), ('stage_id.probability', 'in', ['100', '0'])])
                for lead_id in lead_ids:
                    if not lead_id.multi_dept:
                        lead_id.write({'bu_revenue': lead_id.planned_revenue,
                                       'bu_revenue_for': lead_id.department_id.name})
                    else:
                        bu_revenue_ids = bu_revenue_lineObj.sudo().search([('department_id', '=', department_id)])
                        if bu_revenue_ids:
                            for bu_revId in bu_revenue_ids:
                                bu_revId.lead_id.sudo().write({'bu_revenue': bu_revId.planned_revenue,
                                                               'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = 'Win/Loss/On Hold'

        if self.menu == '13':  # Active pipe Summary
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_form").id
            domain += [('department_id', '=', self.department_id.id)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'),
                                               ('stage_id.probability', 'in', ['100', '0'])])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.write({'bu_revenue': bu_revId.planned_revenue,
                                                            'from_gss_menu': True,
                                                            'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})

            model = 'bu.active.pipe'
            name = 'BU Active Pipe Summary'

        if self.menu == '14':  # Principal Contacts
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_form").id
            model = 'principal.contact'
            name = 'Principal Contact'

        if self.menu:
            return {
                'type': 'ir.actions.act_window',
                'name': name,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': model,
                'domain': domain,
                'views': [(tree_id, 'tree'), (form_id, 'form'), (kanban_id, 'kanban'), (graph_id, 'graph')],
                'target': 'current',
                'context': context,
            }
        else:
            raise exceptions.ValidationError("Please select Menu")


class bdm_review_wizard(models.Model):
    _name = 'bdm.review.wizard'
    _description = 'BDM Review Wizard'
    _order = "id desc"

    AVAILABLE_MENUS = [
        ('0', 'BU Target v/s Achievement (OB & Revenue)'),
        ('1', 'BU Pipeline Build'),
        ('2', 'Opportunities - Active pipe 17-18'),
        ('13', 'BU Opportunities - Active pipe 17-18'),
        ('3', '90 Days - Active pipe 17-18'),
        ('4', 'Called Deal'),
        ('5', 'Review Action Points'),
        ('6', 'Slippage'),
        ('7', 'OMM Dashboard'),
        ('8', 'OMM Mismatch'),
        ('9', 'Account Activity'),
        ('10', 'BU Account Mapping'),
        ('11', 'Principal Touch Point'),
        ('14', 'Principal Contact'),
        ('12', 'Win/Loss/On Hold'),
    ]

    @api.model
    def _get_department_values(self):
        department_id = self.env['hr.department'].search([('parent', '=', False),
                                                          ('dept_main_category', '=', 'Non Support'),
                                                          ('bdm_ids', 'in', [self._uid])])
        department_id = department_id and department_id[0].id or False
        return department_id

    user_id = fields.Many2one('res.users', 'Login user', default=lambda self: self.env.user)
    country_id = fields.Many2one('res.country', 'Country')
    call_deal_quarter = fields.Selection(AVAILABLE_QUARTERS, 'Call Deal Quarter')
    department_id = fields.Many2one('hr.department', 'Business Unit',
                                    default=lambda self: self._get_department_values())
    menu = fields.Selection(AVAILABLE_MENUS, 'Menu')

    @api.multi
    def show_results(self):
        data_pool = self.env['ir.model.data']
        context = self._context
        domain = []
        form_id = False
        tree_id = False
        kanban_id = False
        graph_id = False
        model = False
        name = ''
        crm_leadObj = self.env['crm.lead']
        bu_revenue_lineObj = self.env['crm.lead.revenue.ratio']
        if not self.department_id:
            raise exceptions.ValidationError("Please select BU")
        if self.menu == '0':  # BU Target v/s Achievement (OB & Revenue)
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_order_booking_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.bu_order_booking_kanban").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'bu.order.booking'
            name = 'BU OB & Revenue - Target vs Achievement'

        if self.menu == '1':  # BU Pipeline Build
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_pipeline_build_form").id
            domain += [('department_id', '=', self.department_id.id)]
            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadIds in lead_ids:
                        if leadIds.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.sudo().search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revIds in bu_revenue_ids:
                                    bu_revIds.lead_id.sudo().write({'bu_revenue': bu_revIds.planned_revenue,
                                                                    'from_gss_menu': True,
                                                                    'bu_revenue_for': self.department_id.name})
                        else:
                            if leadIds.department_id.id == department_id:
                                leadIds.write({'bu_revenue': leadIds.planned_revenue, 'from_gss_menu': True,
                                               'bu_revenue_for': self.department_id.name})

            model = 'bu.pipeline.build'
            name = 'BU Pipeline Build'

        if self.menu == '2':  # Opportunities - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('this_year', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.sudo().search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revIds in bu_revenue_ids:
                                    bu_revIds.lead_id.sudo().write({'bu_revenue': bu_revIds.planned_revenue,
                                                                    'from_gss_menu': True,
                                                                    'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = 'Opportunities - Active pipe'

        if self.menu == '3':  # 90 Days - Active pipe
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('ninety_days', '=', True),
                       ('stage_id.probability', '!=', 0), ('stage_id.probability', '!=', 100)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            bu_revenue_ids = bu_revenue_lineObj.sudo().search([('department_id', '=', department_id)])
                            if bu_revenue_ids:
                                for bu_revId in bu_revenue_ids:
                                    bu_revId.lead_id.sudo().write({'bu_revenue': bu_revId.planned_revenue,
                                                                   'from_gss_menu': True,
                                                                   'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = '90 Days - Active pipe'

        if self.menu == '4':  # Called Deals
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('show_call_deals', '=', True),
                       ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0'),]
            if self.call_deal_quarter:
                domain += [('bu_call_deal_quarter', '=', self.call_deal_quarter)]

            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search([('type', '=', 'opportunity'), ('stage_id.probability', '<', '100'),
                                               ('stage_id.probability', '>', '0')])
                if lead_ids:
                    for leadId in lead_ids:
                        if leadId.multi_dept:
                            seller_bu_revenue_ids = bu_revenue_lineObj.sudo().search(
                                [('department_id', '=', department_id)])
                            if seller_bu_revenue_ids:
                                for bu_revId in seller_bu_revenue_ids:
                                    bu_revId.lead_id.sudo().write({'bu_revenue': bu_revId.planned_revenue,
                                                                   'from_gss_menu': True,
                                                                   'bu_revenue_for': self.department_id.name})
                        else:
                            if leadId.department_id.id == department_id:
                                leadId.write({'bu_revenue': leadId.planned_revenue,
                                              'from_gss_menu': True,
                                              'bu_revenue_for': self.department_id.name})
            model = 'crm.lead'
            name = 'Called Deals'

        if self.menu == '5':  # Plan of Action
            tree_id = self.env.ref("crm_dashboard_jmr.view_plan_action_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_plan_action_form").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'plan.action'
            name = 'Plan of Action'

        if self.menu == '6':  # Slippage
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id
            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('slippage', '=', True),
                       ('stage_id.probability', '<', '100'), ('stage_id.probability', '>', '0')]
            model = 'crm.lead'
            name = 'Slippage'

        if self.menu == '7':  # OMM Dashboard
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'crm.omm'
            name = 'OMM Dashboard'

        if self.menu == '8':  # OMM Mismatch
            tree_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_mismatch_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_crm_omm_graph").id
            domain += [('department_id', '=', self.department_id.id), ('is_omm_mismatch', '=', True)]
            model = 'crm.omm'
            name = 'OMM Mismatch'

        if self.menu == '9':  # TODO: Account Activity
            tree_id = self.env.ref("crm_dashboard_jmr.view_Account_activity_tree").id
            form_id = self.env.ref("crm_jmr.view_partner_account_form").id
            domain += [('department_id', '=', self.department_id.id),
                       ('is_company', '=', True), ('ninety_days', '=', True)]
            model = 'res.partner'
            name = 'Account Activity'

        if self.menu == '10':  # BU Account Mapping
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_form").id
            kanban_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_kanban").id
            graph_id = self.env.ref("crm_dashboard_jmr.view_bu_account_mapping_graph").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'bu.account.mapping'
            name = 'BU Account Mapping'

        if self.menu == '11':  # Principal Touch Point
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_touch_point_form").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'principal.touch.point'
            name = 'Principal Touch Point'

        if self.menu == '12':  # Win/Loss/On Hold
            tree_id = self.env.ref("crm_dashboard_jmr.crm_case_tree_view_oppor_dashboard").id
            form_id = self.env.ref("crm.crm_case_form_view_oppor").id
            kanban_id = self.env.ref("crm_dashboard_jmr.crm_case_kanban_view_leads_dashboard").id
            graph_id = self.env.ref("crm.crm_case_graph_view_leads").id

            domain += ['|', ('department_id', '=', self.department_id.id),
                       ('multi_department_ids', 'in', [self.department_id.id]), ('wlo_opportunities', '=', True)]
            # Update Multi BU Revenue Value
            department_id = self.department_id and self.department_id.id or False
            if department_id:
                lead_ids = crm_leadObj.search(['|', ('department_id', '=', self.department_id.id),
                                               ('multi_department_ids', 'in', [self.department_id.id]),
                                               ('type', '=', 'opportunity'),
                                               ('stage_id.probability', 'in', ['100', '0'])])
                for lead_id in lead_ids:
                    if not lead_id.multi_dept:
                        lead_id.write({'bu_revenue': lead_id.planned_revenue,
                                       'bu_revenue_for': lead_id.department_id.name})
                    else:
                        bu_revenue_ids = bu_revenue_lineObj.sudo().search([('department_id', '=', department_id)])
                        if bu_revenue_ids:
                            for bu_revId in bu_revenue_ids:
                                bu_revId.lead_id.sudo().write({'bu_revenue': bu_revId.planned_revenue,
                                                               'bu_revenue_for': self.department_id.name})

            model = 'crm.lead'
            name = 'Win/Loss/On Hold'

        if self.menu == '13':  # Active pipe Summary
            tree_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_bu_active_pipe_form").id
            domain += [('department_id', '=', self.department_id.id)]
            model = 'bu.active.pipe'
            name = 'BU Active Pipe Summary'

        if self.menu == '14':  # Principal Contacts
            tree_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_tree").id
            form_id = self.env.ref("crm_dashboard_jmr.view_principal_contact_form").id
            model = 'principal.contact'
            name = 'Principal Contact'

        if self.menu:
            return {
                'type': 'ir.actions.act_window',
                'name': name,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': model,
                'domain': domain,
                'views': [(tree_id, 'tree'), (form_id, 'form'), (kanban_id, 'kanban'), (graph_id, 'graph')],
                'target': 'current',
                'context': context,
            }
        else:
            raise exceptions.ValidationError("Please select Menu")