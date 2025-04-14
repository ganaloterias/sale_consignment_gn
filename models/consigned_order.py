# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsignedOrder(models.Model):
    _name = 'consigned.order'
    _description = 'Consigned Order'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: 'New')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    settlement_date = fields.Date(string='Settlement Date')
    list_prices = fields.Boolean(string='List Prices', default=True)
    
    order_line_ids = fields.One2many('consigned.order.line', 'order_id', string='Order Lines')
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('consigned.order') or 'New'
        return super(ConsignedOrder, self).create(vals) 