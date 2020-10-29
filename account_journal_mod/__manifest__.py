# -*- coding: utf-8 -*-
{
    'name': "Account Journal Mod",

    'summary': """
        Account journal mod for Sanwa""",

    'description': """
        Account journal mod for Sanwa
    """,

    'author': "butirpadi@gmail.com",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'purchase', 'purchase_stock', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/account_journal_view.xml',
        # 'views/bank_statement_view.xml',
        'views/account_move_view.xml',
        'views/res_company.xml',
        'views/purchase_order_view.xml',
        # wizard
        'wizards/balance_purchase_report_wizard.xml',
        # reports
        # 'reports/voucher_report.xml',
        # 'reports/web_report.xml',
        'reports/bukti_jurnal_report.xml',
        'reports/journal_voucher_report.xml',
        'reports/balance_purchase_report.xml',
        'reports/purchase_report.xml',
        'reports/action_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
