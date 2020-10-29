from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_statement_auto_sequence = fields.Boolean(
        string='Auto Sequence on Bank Statement', default=False)
    bankstatement_seq_code = fields.Many2one(
        comodel_name='ir.sequence', string='Bank Statement Sequence')

    @api.model
    def create(self, vals):
        # Add code here
        res = super(AccountJournal, self).create(vals)

        if res.bank_statement_auto_sequence:
            # create sequence
            bs_seq = self.env['ir.sequence'].create({
                'name': 'BS' + str(res.id),
                'implementation': 'no_gap',
                'prefix': 'BS' + str(res.id) + '/%(range_year)s/%(month)s/',
                'padding': 4,
                'number_increment': 1,
                'code': 'BS' + str(res.id) + '.seq.code'
            })
            res.bankstatement_seq_code = bs_seq
        return res

    @api.multi
    def write(self, vals):
        if 'bank_statement_auto_sequence' in vals:
            if vals['bank_statement_auto_sequence']:
                if not self.bankstatement_seq_code:
                    bs_seq = self.env['ir.sequence'].create({
                        'name': 'BS' + str(self.id),
                        'implementation': 'no_gap',
                        'prefix': 'BS' + str(self.id) + '/%(range_year)s/%(month)s/',
                        'padding': 4,
                        'number_increment': 1,
                        'code': 'BS' + str(self.id) + '.seq.code'
                    })
                    self.bankstatement_seq_code = bs_seq

        return super(AccountJournal, self).write(vals)
