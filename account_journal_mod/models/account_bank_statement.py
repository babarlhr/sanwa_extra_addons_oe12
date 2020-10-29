from odoo import api, fields, models, _
from pprint import pprint


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    auto_seq_on_bankstatement = fields.Boolean(
        string='Auto Sequence', related='journal_id.bank_statement_auto_sequence')
    no_cek_bank = fields.Char('No. Cek/Bank')
    notes = fields.Text('Notes')

    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
              'delapan', 'sembilan', 'sepuluh', 'sebelas']

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
        num = abs(self.total_entry_encoding)
        terbilang = ""
        t = self.terbilang_(num)
        while '' in t:
            t.remove('')
        terbilang = ' '.join(t)
        return terbilang

    @api.model
    def create(self, vals):
        res = super(AccountBankStatement, self).create(vals)

        print(res.journal_id.name)
        if res.journal_id.bank_statement_auto_sequence:
            # generate auto reference
            print('------------------------')
            seq_code = res.journal_id.bankstatement_seq_code.code
            print('Journal : ' + str(res.journal_id.name))
            print('Sequence Code : ' + seq_code)
            pprint(res.journal_id.bankstatement_seq_code)
            code_name = ""

            if 'company_id' in vals:
                code_name = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(seq_code) or _('New')
            else:
                code_name = self.env['ir.sequence'].next_by_code(
                    seq_code) or _('New')

            res.name = code_name
            print(code_name)
            print('-----------------------------')

        return res

    def get_partner(self):
        my_partner = ""
        for line in self.line_ids:
            if line.partner_id:
                my_partner = line.partner_id.name
                exit

        return my_partner
    
    def get_account(self, statement_line_id):
        statement_line = self.env['account.bank.statement.line'].search([('id','=', statement_line_id)])
        account_move_line = self.env['account.move.line'].search(['&','&',('statement_id','=',statement_line.statement_id.id), ('statement_line_id','=',statement_line_id),('account_id','!=',self.journal_id.default_debit_account_id.id)])
        
        return account_move_line.account_id
