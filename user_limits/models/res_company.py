# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
	_inherit = 'res.company'

	max_limit = fields.Integer('Max Users Limit')
