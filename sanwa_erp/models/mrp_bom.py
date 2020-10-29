from odoo import fields, api, models
from datetime import datetime
from odoo import tools
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class additional_field(models.Model):
    _inherit = "mrp.bom"


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_qty = fields.Float(digits=(12, 9))
