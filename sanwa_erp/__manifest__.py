# -*- coding: utf-8 -*-
{
    'name': "Custom ERP PT. Sanwa Parts Indonesia",

    'summary': """
        Custom modules untuk PT. Sanwa Parts Indonesia""",

    'description': """
        Custom modules untuk PT. Sanwa Parts Indonesia
    """,

    'author': "Team",
    'website': "http://www.kikinsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ERP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'purchase', 'stock', 'mrp', 'account_accountant'],

    # always loaded
    'data': [
        'views/product_template.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': True
}
