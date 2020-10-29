from odoo import fields, api, models
from datetime import datetime
from odoo import tools
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    scrap_qty = fields.Float(string="Quantity", digits=(12, 5))
