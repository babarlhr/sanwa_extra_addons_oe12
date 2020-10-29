from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'mail.thread']

    no_cek_bank = fields.Char('No.Cek/Bank Rek', track_visibility='always')
    date_voucher = fields.Date('Voucher Date', track_visibility='always')

    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
              'delapan', 'sembilan', 'sepuluh', 'sebelas']

    journal_currency_rate = fields.Float(
        string='Currency Rate', compute="_compute_journal_currency_rate", store=True)
    amount_currency = fields.Monetary(string="Amount Currency", compute="_compute_amount_currency", store=True)
    state = fields.Selection(track_visibility='onchange')
    date = fields.Date(track_visibility='always')
    ref = fields.Char(track_visibility='always')

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return 'account_journal_mod.mt_state_draft'
        elif 'state' in init_values and self.state == 'posted':
            return 'account_journal_mod.mt_state_posted'
        return super(AccountMove, self)._track_subtype(init_values)


    @api.multi
    @api.depends('line_ids.amount_currency')
    def _compute_amount_currency(self):
        for move in self:
            total = 0.0
            for line in move.line_ids:
                if line.amount_currency > 0:
                    total += line.amount_currency
            move.amount_currency = total
        

    @api.depends('journal_id')
    def _compute_journal_currency_rate(self):
        for rec in self:
            if rec.journal_id.currency_id:
                rec.journal_currency_rate = rec.journal_id.currency_id.rate

    def terbilang_(self, n):
        if n >= 0 and n <= 11:
            hasil = [self.satuan[int(n)]]
        elif n >= 12 and n <= 19:
            hasil = self.terbilang_(n % 10) + ['belas']
        elif n >= 20 and n <= 99:
            hasil = self.terbilang_(
                n / 10) + ['puluh'] + self.terbilang_(n % 10)
        elif n >= 100 and n <= 199:
            hasil = ['seratus'] + self.terbilang_(n - 100)
        elif n >= 200 and n <= 999:
            hasil = self.terbilang_(n / 100) + \
                ['ratus'] + self.terbilang_(n % 100)
        elif n >= 1000 and n <= 1999:
            hasil = ['seribu'] + self.terbilang_(n - 1000)
        elif n >= 2000 and n <= 999999:
            hasil = self.terbilang_(n / 1000) + \
                ['ribu'] + self.terbilang_(n % 1000)
        elif n >= 1000000 and n <= 999999999:
            hasil = self.terbilang_(n / 1000000) + \
                ['juta'] + self.terbilang_(n % 1000000)
        else:
            hasil = self.terbilang_(n / 1000000000) + \
                ['milyar'] + self.terbilang_(n % 100000000)
        return hasil

    def get_terbilang(self):
        # num = self.amount
        num = 0.0
        if self.journal_id.currency_id:
            num = self.amount_currency
        #     if self.journal_currency_rate > 1 :
        #         num = self.amount / self.journal_currency_rate
        #     else:
        #         num = self.amount * self.journal_currency_rate
        else:
            num = self.amount

        print('Amount Terbilang')
        print(str(num))

        terbilang = ""
        t = self.terbilang_(num)
        while '' in t:
            t.remove('')
        terbilang = ' '.join(t)
        return terbilang

    # def can_print_voucher(self):
    #     filter_line = filter(,self.line_ids)

    def get_cashbank_account(self):
        cashbank_acc_type_model_data = self.env['ir.model.data'].search(
            [('name', '=', 'data_account_type_liquidity')])
        cashbank_acc_type = self.env['account.account.type'].search(
            [('id', '=', cashbank_acc_type_model_data.res_id)])

        my_cashbank_acc = None
        for line in self.line_ids:
            if line.account_id.user_type_id.id == cashbank_acc_type.id:
                my_cashbank_acc = line.account_id
                exit

        return my_cashbank_acc

    def get_partner(self):
        my_partner = None
        for line in self.line_ids:
            my_partner = line.partner_id
            exit

        return my_partner

    def can_print_voucher(self):
        cashbank_acc_found = 0
        cashbank_acc_type_model_data = self.env['ir.model.data'].search(
            [('name', '=', 'data_account_type_liquidity')])
        cashbank_acc_type = self.env['account.account.type'].search(
            [('id', '=', cashbank_acc_type_model_data.res_id)])

        for line in self.line_ids:
            if line.account_id.user_type_id.id == cashbank_acc_type.id:
                cashbank_acc_found = cashbank_acc_found + 1

        if cashbank_acc_found == 1:
            return True
        else:
            return False
