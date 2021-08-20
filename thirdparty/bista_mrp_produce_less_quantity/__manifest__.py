# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

{
    'name': 'Bista MRP Less Quantity Consumption',
    'version': '1.0',
    'sequence': 1,
    'category': 'Manufacturing',
    'summary': "This Module provide custom MPR feature.",
    'description': """
            This Module has following Features
            1. Can modify Actual Output Quantity to produce in the manufacturing
             order. 
    """,
    'website': 'https://www.bistasolutions.com',
    'author': 'Bista Solutions',
    'images': [],
    'depends': ['mrp_workorder', 'mrp_account_enterprise'],
    'data': [
        'views/mrp_production_views.xml',
        'views/mrp_workorder_views.xml',
    ],
    'application': True,
    'installable': True,
}
