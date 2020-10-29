from odoo import api, fields, models


class ManufacturingOrder(models.Model):
    _inherit = "mrp.production"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('planned', 'Planned'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='State',
        copy=False, track_visibility='onchange')

    # state = fields.Selection(selection_add=[('draft', 'Draft')])

    @api.multi
    def action_draft(self):
        
        self.move_raw_ids.write({'is_done':False})
        self.move_raw_ids = False
        self.move_finished_ids = False
        self.write({'state': 'draft'})
        return True

    @api.multi
    def action_confirmed(self):
        self._generate_moves()
        self.write({'state': 'confirmed'})
        return True