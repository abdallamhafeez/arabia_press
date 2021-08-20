# -*- coding: utf-8 -*-
{
    'name': "MRP Request",
    'summary': """ Create Routing And Bom In Manufacturing Requests """,
    'author': "Younis Mostafa Khalaf",
    'website': "http://linkedin.com/in/younis-mostafa-6b78ab127",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['base', 'mrp_production_request', 'work_center',
                'bi_odoo_process_costing_manufacturing', 'mrp',
                'close_form_after_save'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_production_request.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
