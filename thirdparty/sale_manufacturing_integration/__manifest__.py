# -*- coding: utf-8 -*-
{
    'name': "Sale Manufacturing Integration",
    'summary': """ Sale Manufacturing Integration""",
    'author': "Younis Mostafa Khalaf",
    'website': "http://linkedin.com/in/younis-mostafa-6b78ab127",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['base', 'mrp_production_request', 'sale', 'mrp_request', 'mrp'],
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_layout.xml',
        'report/production_request_operation_order.xml',
        'report/production_request_temp.xml',
        'report/report_definition.xml',
        'views/mrp_production_request.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
