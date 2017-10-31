# -*- coding: utf-8 -*-

{
    'name': 'Easy to Create User',
    'version': '1.0',
    'author': 'Hareesh Gopalar',
    'category': 'Technical Settings',
    'summary': 'Easy to Create/Add Users',
    'description': """
CRM Sales Target
====================================

Description:
------------
Easy to Create/Add Users
    """,
    'depends': [
                'base',
                ],
    'data': [
             'security/res_groups_data.xml',
             # 'security/ir.model.access.csv',
             'views/user_create_wizard_view.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
