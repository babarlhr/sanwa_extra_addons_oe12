from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    fax = fields.Char('Fax')
