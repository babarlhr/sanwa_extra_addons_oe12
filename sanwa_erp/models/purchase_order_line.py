from odoo import fields, api, models


class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    product_qty = fields.Float(
        string='Quantity', digits=(12, 2), required=True)
    qty_balance = fields.Float(
        string="Balance Qty", readonly=True, compute="compute_qty_balance")

    @api.depends('product_qty', 'qty_received')
    def compute_qty_balance(self):
        for row in self:
            row.qty_balance = row.product_qty - row.qty_received
