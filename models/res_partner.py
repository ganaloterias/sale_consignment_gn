# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_consignment_partner = fields.Boolean(
        string='Is Consignment Partner',
        help='Check this if this partner works with consignment inventory'
    )

    consignment_stock_ids = fields.One2many(
        'consigned.partner.stock',
        'partner_id',
        string='Consignment Stock'
    )

    consignment_order_ids = fields.One2many(
        'consigned.order',
        'partner_id',
        string='Consignment Orders'
    )

    total_consigned_quantity = fields.Integer(
        string='Total Consigned Quantity',
        compute='_compute_total_consigned_quantity',
        help='Total quantity of consigned products for this partner'
    )

    @api.depends('consignment_stock_ids', 'consignment_stock_ids.quantity')
    def _compute_total_consigned_quantity(self):
        for partner in self:
            partner.total_consigned_quantity = sum(
                stock.quantity for stock in partner.consignment_stock_ids
            )