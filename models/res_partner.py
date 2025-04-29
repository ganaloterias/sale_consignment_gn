# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    consignment_stock_ids = fields.One2many(
        'consigned.partner.stock',
        'partner_id',
        string='Consignment Stock'
    )

    consigned_commission_ids = fields.One2many(
        'consigned.commission',
        'partner_id',
        string='Consigned Commissions'
    )

    consignment_order_ids = fields.One2many(
        'consigned.order',
        'partner_id',
        string='Consignment Orders'
    )

    consignment_count = fields.Integer(
        string='Consignment Count',
        compute='_compute_consignment_count',
        help='Total quantity of consigned products for this partner'
    )

    @api.depends('consignment_order_ids')
    def _compute_consignment_count(self):
        for partner in self:
            partner.consignment_count = len(partner.consignment_order_ids)

    def action_view_consignment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Consignments',
            'res_model': 'consigned.order',
            'view_mode': 'list,kanban,form',
            'domain': [('partner_id', '=', self.id)],
        }
