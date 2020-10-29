from odoo import api, fields, models
from pprint import pprint


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    currency_rate = fields.Float(string='Currency Rate')
    currency_debit = fields.Monetary(string='Debit')
    currency_credit = fields.Monetary(string='Credit')

    @api.onchange('amount_currency', 'currency_id', 'account_id')
    def _onchange_amount_currency(self):
        # '''Recompute the debit/credit based on amount_currency/currency_id and date.
        # However, date is a related field on account.move. Then, this onchange will not be triggered
        # by the form view by changing the date on the account.move.
        # To fix this problem, see _onchange_date method on account.move.
        # '''
        # for line in self:
        #     company_currency_id = line.account_id.company_id.currency_id
        #     amount = line.amount_currency
        #     if line.currency_id and company_currency_id and line.currency_id != company_currency_id:
        #         amount = line.currency_id._convert(amount, company_currency_id, line.company_id, line.date or fields.Date.today())
        #         line.debit = amount > 0 and amount or 0.0
        #         line.credit = amount < 0 and -amount or 0.0
        res = super(AccountMoveLine, self)._onchange_amount_currency()
        
        # get currency rate
        for rec in self:
            if rec.currency_id:
                rec.currency_rate = rec.currency_id.rate 
                
                # set currency debit credit
                rec.currency_debit = rec.amount_currency > 0 and rec.amount_currency or 0.0
                rec.currency_credit = rec.amount_currency < 0 and -rec.amount_currency or 0.0
                
                # # set default debit/credit field
                # amount = self.currency_id._convert(self.amount_currency, self.account_id.company_id.currency_id, self.company_id, self.date or fields.Date.today())
                # self.debit = amount > 0 and amount or 0.0
                # self.credit = amount < 0 and -amount or 0.0
        
            
        return res
