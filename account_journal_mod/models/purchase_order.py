from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    incoterm_desc = fields.Char('Incoterm Desc')
    shipment_by = fields.Char('Shipment By')
    eta_delivery = fields.Date(string='ETA Delivery')
    eta_point = fields.Char(string='ETA Point')
    production_month_str = fields.Char(string='Production Month')

    