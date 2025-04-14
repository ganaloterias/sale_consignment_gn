# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsignedMove(models.Model):
    _name = 'consigned.move'
    _description = 'Consigned Move'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: 'New')
    order_id = fields.Many2one('consigned.order', string='Order')
    type = fields.Selection([
        ('in', 'Incoming'),
        ('out', 'Outgoing'),
        ('return', 'Return')
    ], string='Type', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    related_order_line_id = fields.Many2one('consigned.order.line', string='Related Order Line',
                                          compute='_compute_related_order_line', store=True)
    move_line_ids = fields.One2many('consigned.move.line', 'move_id', string='Move Lines')

    @api.depends('order_id', 'product_id')
    def _compute_related_order_line(self):
        for move in self:
            if move.order_id and move.product_id:
                move.related_order_line_id = self.env['consigned.order.line'].search([
                    ('order_id', '=', move.order_id.id),
                    ('product_id', '=', move.product_id.id)
                ], limit=1)
            else:
                move.related_order_line_id = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('consigned.move') or 'New'
        return super(ConsignedMove, self).create(vals) 