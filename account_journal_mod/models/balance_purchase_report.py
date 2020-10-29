from odoo import models, fields, api, _
from odoo.exceptions import UserError
from pprint import pprint

class BalancePurchaseReport(models.TransientModel):
    _name = 'balance.purchase.report'

    name = fields.Char()
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    purchase_order_line_ids = fields.Many2many(
        comodel_name='purchase.order.line',
        relation='balance_report_purchase_rel',
        column1='balance_purchase_report_id',
        column2='purchase_order_line_id',
        string='Purchase Order Line'
    )

    def action_submit(self):
        self.write({
            'name': 'Balance PO Report'
        })

        po_ids = self.env['purchase.order'].search(
            [('date_order', '>=', self.date_start), ('date_order', '<=', self.date_end)])

        add_po = []
        for po in po_ids:
            for line in po.order_line:
                print('add order line')
                print('-------------------------------')
                # self.env['balance.purchase.report'].search([('id', '=', self.id)]).write({
                add_po.append((4,line.id))
        pprint(add_po)
        self.write({
                    'purchase_order_line_ids': add_po
                })

        # show html report
        return self.env.ref('account_journal_mod.action_report_balance_purchase').report_action(self)
