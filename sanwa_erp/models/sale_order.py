from odoo import fields, api, models


class sale_order_line(models.Model):
    _inherit = "sale.order"

    commitment_date = fields.Datetime(string="Due Date")
