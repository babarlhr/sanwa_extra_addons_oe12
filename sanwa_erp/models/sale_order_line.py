from odoo import fields, api, models


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        'SO Date', related='order_id.date_order', readonly=True)
    due_date = fields.Datetime(
        string="Due Date", related='order_id.commitment_date', readonly=True)
    qty_balance = fields.Float(
        string="Balance Qty", readonly=True, compute="compute_qty_balance")

    @api.depends('product_uom_qty', 'qty_delivered')
    def compute_qty_balance(self):
        for row in self:
            row.qty_balance = row.product_uom_qty - row.qty_delivered
