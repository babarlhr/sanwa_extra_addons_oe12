from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    price_unit = fields.Float(digits=(12, 6))

    def _set_currency(self):
        print("{:.6f}".format(self.price_unit))
        # import traceback;
        # traceback.print_stack()
        # company = self.invoice_id.company_id
        # currency = self.invoice_id.currency_id
        # if company and currency:
        #     if company.currency_id != currency:
        #         self.price_unit = self.price_unit * currency.with_context(
        #             dict(self._context or {}, date=self.invoice_id.date_invoice)).rate


    def _set_taxes(self):
        """ Used in on_change to set taxes and price"""
        self.ensure_one()

        # Keep only taxes of the company
        company_id = self.company_id or self.env.user.company_id

        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            taxes = self.product_id.taxes_id.filtered(lambda
                                                          r: r.company_id == company_id) or self.account_id.tax_ids or self.invoice_id.company_id.account_sale_tax_id
        else:
            taxes = self.product_id.supplier_taxes_id.filtered(lambda
                                                                   r: r.company_id == company_id) or self.account_id.tax_ids or self.invoice_id.company_id.account_purchase_tax_id

        self.invoice_line_tax_ids = fp_taxes = self.invoice_id.fiscal_position_id.map_tax(taxes, self.product_id,
                                                                                          self.invoice_id.partner_id)

        fix_price = self.env['account.tax']._fix_tax_included_price
        if self.invoice_id.type in ('in_invoice', 'in_refund'):
            prec = self.env['decimal.precision'].precision_get('Product Price')
            params = {'invoice_id': self.invoice_id}
            seller = self.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=self.quantity,
                date=self.invoice_id.date_invoice and self.invoice_id.date_invoice.date(),
                uom_id=self.uom_id,
                params=params)

            price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                                 self.product_id.supplier_taxes_id,
                                                                                 self.invoice_line_tax_ids,
                                                                                 self.company_id) if seller else 0.0

            if price_unit and seller and self.invoice_id.currency_id and seller.currency_id != self.invoice_id.currency_id:
                price_unit = seller.currency_id._convert(
                    price_unit, self.invoice_id.currency_id, self.invoice_id.company_id,
                    self.invoice_id.date_invoice or fields.Date.today())

            if seller and self.uom_id and seller.product_uom != self.uom_id:
                price_unit = seller.product_uom._compute_price(price_unit, self.uom_id)

            self.price_unit = price_unit
            # print("{:.6f}".format(self.price_unit))

        else:
            self.price_unit = fix_price(self.product_id.lst_price, taxes, fp_taxes)
            self._set_currency()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        domain = {}
        if not self.invoice_id:
            return

        part = self.invoice_id.partner_id
        fpos = self.invoice_id.fiscal_position_id
        company = self.invoice_id.company_id
        currency = self.invoice_id.currency_id
        type = self.invoice_id.type

        if not part:
            warning = {
                'title': _('Warning!'),
                'message': _('You must first select a partner.'),
            }
            return {'warning': warning}

        if not self.product_id:
            if type not in ('in_invoice', 'in_refund'):
                self.price_unit = 0.0
            domain['uom_id'] = []
        else:
            self_lang = self
            if part.lang:
                self_lang = self.with_context(lang=part.lang)

            product = self_lang.product_id
            account = self.get_invoice_line_account(type, product, fpos, company)
            if account:
                self.account_id = account.id
            self._set_taxes()

            product_name = self_lang._get_invoice_line_name_from_product()
            if product_name != None:
                self.name = product_name

            if not self.uom_id or product.uom_id.category_id.id != self.uom_id.category_id.id:
                self.uom_id = product.uom_id.id
            domain['uom_id'] = [('category_id', '=', product.uom_id.category_id.id)]

            if company and currency:

                if self.uom_id and self.uom_id.id != product.uom_id.id:
                    self.price_unit = product.uom_id._compute_price(self.price_unit, self.uom_id)
                    # print("{:.6f}".format(self.price_unit))

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        warning = {}
        result = {}
        if not self.uom_id:
            self.price_unit = 0.0

        if self.product_id and self.uom_id:
            if self.invoice_id.type in ('in_invoice', 'in_refund'):
                params = {'invoice_id': self.invoice_id}
                seller = self.product_id._select_seller(
                    partner_id=self.partner_id,
                    quantity=self.quantity,
                    date=self.invoice_id.date_invoice and self.invoice_id.date_invoice.date(),
                    uom_id=self.uom_id,
                    params=params)

                price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                                     self.product_id.supplier_taxes_id,
                                                                                     self.invoice_line_tax_ids,
                                                                                     self.company_id) if seller else 0.0

                if price_unit and seller and self.invoice_id.currency_id and seller.currency_id != self.invoice_id.currency_id:
                    price_unit = seller.currency_id._convert(
                        price_unit, self.invoice_id.currency_id, self.invoice_id.company_id,
                        self.invoice_id.date_invoice or fields.Date.today())

                if seller and self.uom_id and seller.product_uom != self.uom_id:
                    price_unit = seller.product_uom._compute_price(price_unit, self.uom_id)

            else:
                price_unit = self.product_id.lst_price
            self.price_unit = self.product_id.uom_id._compute_price(price_unit, self.uom_id)
            self._set_currency()

            if self.product_id.uom_id.category_id.id != self.uom_id.category_id.id:
                warning = {
                    'title': _('Warning!'),
                    'message': _(
                        'The selected unit of measure has to be in the same category as the product unit of measure.'),
                }
                self.uom_id = self.product_id.uom_id.id
        if warning:
            result['warning'] = warning
        return result