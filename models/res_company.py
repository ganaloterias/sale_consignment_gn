# -*- coding: utf-8 -*-

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'
    _check_company_auto = True


    consignment_journal_id = fields.Many2one(
        'account.journal',
        string='Consignment Journal'
    )
    
    default_consignment_account_id = fields.Many2one(
        'account.account',
        string='Default Consignment Account'
    )

    consignment_days_limit = fields.Integer(
        string='Consignment Days Limit',
        default=30
    )

    auto_validate_consignment = fields.Boolean(
        string='Auto-validate Consignment Orders',
        default=False
    )