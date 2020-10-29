# -*- coding: utf-8 -*-
from odoo import http

# class AccountJournalMod(http.Controller):
#     @http.route('/account_journal_mod/account_journal_mod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_journal_mod/account_journal_mod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_journal_mod.listing', {
#             'root': '/account_journal_mod/account_journal_mod',
#             'objects': http.request.env['account_journal_mod.account_journal_mod'].search([]),
#         })

#     @http.route('/account_journal_mod/account_journal_mod/objects/<model("account_journal_mod.account_journal_mod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_journal_mod.object', {
#             'object': obj
#         })