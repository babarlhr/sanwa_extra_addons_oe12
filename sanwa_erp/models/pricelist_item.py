from odoo import fields, api, models

from odoo.addons import decimal_precision as dp


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    fixed_price = fields.Float(
        'Fixed Price', digits=dp.get_precision('Product Price'))
