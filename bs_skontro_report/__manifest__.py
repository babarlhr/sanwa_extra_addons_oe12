# -*- coding: utf-8 -*-
{
    'name': "Balance Sheet Skontro",

    'summary': """
        Balance sheet skontro""",

    'description': """
        Balance sheet bentuk skontro
    """,

    'author': "butirpadi",
    'website': "https://www.github.com/butirpadi",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/account_pdf_reports.xml',
        'views/account_reports_settings.xml',
        # 'wizards/partner_ledger.xml',
        # 'wizards/general_ledger.xml',
        # 'wizards/trial_balance.xml',
        'wizards/balance_sheet.xml',
        # 'wizards/profit_and_loss.xml',
        # 'wizards/tax_report.xml',
        # 'wizards/aged_partner.xml',
        # 'wizards/journal_audit.xml',
        'reports/report.xml',
        # 'reports/report_partner_ledger.xml',
        # 'reports/report_general_ledger.xml',
        # 'reports/report_trial_balance.xml',
        'reports/report_financial.xml',
        # 'reports/report_tax.xml',
        # 'reports/report_aged_partner.xml',
        # 'reports/report_journal_audit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
