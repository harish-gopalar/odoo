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

{
    'name': 'CRM Dashboard',
    'version': '1.1',
    'author': 'Hareesh Gopalar',
    'category': 'Customer Relationship Management',
    'website': 'http://www.jmrinfotech.com/',
    'summary': 'Sales Target vs Achievements',
    'description': """
CRM Sales Target
====================================

Description:
------------
Sales Target Vs Achievements, Committed Closures.

Before running CRM Dashboard Scheduled Actions, Clean unwanted data from below screens

Menu's: Sales/Sales/Configuration/
        1.Salesperson Hierarchy

        2.SalesPerson Responsibility

Models Inherited:
        1.salesperson.target

        2.manager.users.relation

        3.crm.users.mapping

        4.crm.case.stage

        5.crm.lead
    """,
    'depends': [
                'crm', 'crm_jmr', 'hr_jmr',
                ],
    'data': [
             'security/crm_dashboard_security.xml',
             'security/ir.model.access.csv',
             'views/crm_sales_target.xml',
             'views/crm_committed_closures_view.xml',
             'views/crm_bu_committed_closures_view.xml',
             'views/incentive_simulation_view.xml',
             'views/crm_omm_view.xml',
             'views/crm_omm_mismatch_data_view.xml',
             'views/crm_principal_touch_view.xml',
             'views/bu_achievement_view.xml',
             'views/email_notifications.xml',
             'views/crm_dashboard_view.xml',
             'views/crm_yearly_card_view.xml',
             'views/crm_review_wizard_view.xml',
             'views/crm_plan_action_view.xml',
             'views/crm_account_mapping_view.xml',
             'views/crm_schedule_action_view.xml',
             'views/crm_active_pipe_view.xml',
             'reports/crm_account_summary_view.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
