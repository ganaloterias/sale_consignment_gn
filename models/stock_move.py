# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    consignment_line_id = fields.Many2one(
        'consigned.order.line',
        string='Consignment Line',
        index=True,
        ondelete='set null'
    )

    def _get_source_document(self):
        res = super()._get_source_document()
        return self.sudo().consignment_line_id.order_id or res 