# -*- coding: utf-8 -*-
{
    'name': "Work Center",
    'author': "Younis Mostafa Khalaf",
    'website': "http://linkedin.com/in/younis-mostafa-6b78ab127",
    'summary': """ Create Work Center Type In Work Center """,
    'category': 'Manufacturing',
    'version': '13.0.1.0.0',
    'depends': ['base', 'mrp', 'mrp_account_enterprise'],
    'data': [
        'security/ir.model.access.csv',
        'views/work_center_type.xml',
        'views/mrp_workcenter.xml',
        'views/mrp_routing_workcenter.xml',
        'views/mrp_workorder.xml',
        'report/mrp_cost_structure.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
