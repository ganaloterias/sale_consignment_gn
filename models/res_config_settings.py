# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Consignment Settings
    group_consignment_user = fields.Boolean(
        "Consignment Features",
        implied_group='sale_consignment_gn.group_sale_consignment_user',
        group='base.group_user'
    )

    consignment_days_limit = fields.Integer(
        string='Consignment Days Limit',
        help='Maximum number of days a product can be in consignment',
        related='company_id.consignment_days_limit',
        readonly=False,
        default=30
    )

    auto_validate_consignment = fields.Boolean(
        string='Auto-validate Consignment Orders',
        help='Automatically validate consignment orders upon creation',
        related='company_id.auto_validate_consignment',
        readonly=False
    )

    module_sale_consignment_report = fields.Boolean(
        "Consignment Reports"
    )

    @api.onchange('group_consignment_user')
    def _onchange_group_consignment_user(self):
        if not self.group_consignment_user:
            self.module_sale_consignment_report = False 