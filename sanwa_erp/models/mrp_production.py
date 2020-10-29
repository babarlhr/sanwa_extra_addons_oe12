from odoo import fields, api, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    date_planned_start = fields.Datetime(
        'Production Start', copy=False, default=fields.Datetime.now,
        index=True, required=True,
        states={'confirmed': [('readonly', False)]}, oldname="date_planned")
    origin = fields.Char(
        'PO No.', copy=False,
        help="Reference of the document that generated this production order request.")
