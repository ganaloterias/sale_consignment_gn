# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ConsignedOrderLine(models.Model):
    _name = 'consigned.order.line'
    _description = 'Consigned Order Line'

    order_id = fields.Many2one('consigned.order', string='Order', required=True, ondelete='cascade')

    ## Related fields

    company_id = fields.Many2one('res.company', related='order_id.company_id', store=True, index=True, precompute=True)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True, precompute=True)
    partner_id = fields.Many2one('res.partner', related='order_id.partner_id', store=True, precompute=True)
    state = fields.Selection(related='order_id.state', store=True, precompute=True)
    settlement_date = fields.Date(related='order_id.settlement_date', index=True)

    ## Generic fields
    product_id = fields.Many2one('product.product', string='Product', required=True, domain="[('can_be_consigned', '=', True)]")
    quantity = fields.Integer(string='Quantity', required=True)
    returned_quantity = fields.Integer(string='Returned Quantity', default=0)
    remaining_quantity = fields.Integer(string='Remaining Quantity', compute='_compute_remaining_quantity', store=True)

    ## Commission fields
    commission_type = fields.Char(string='Commission Type')
    commission_value = fields.Float(string='Commission Value')
    commission_amount = fields.Float(string='Commission Amount', store=True)

    ## Pricing fields
    unit_price = fields.Float(string='Unit Price', related='product_id.lst_price')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    to_pay_amount = fields.Float(string='To Pay Amount', compute='_compute_to_pay_amount', store=True)

    """ Movements """
    stock_move_ids = fields.One2many('stock.move', 'consignment_line_id', string='Stock Movements')
    picking_ids = fields.Many2many(
        'stock.picking',
        string='Transfers',
        compute='_compute_picking_ids',
        store=True
    )
    stock_move_count = fields.Integer(string='Movement Count', compute='_compute_movement_count')
    stock_tracking_count = fields.Integer(string='Tracking Count', compute='_compute_tracking_count')
    
    """ Onchange methods """
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Update commission information when product changes."""
        if not self.product_id:
            return

        commission = self._get_or_create_commission()
        
        print(commission)
        if commission:
            self.commission_type = commission.commission_type
            self.commission_value = commission.commission_value
            # Force recompute total_price before calculating commission
            self._compute_total_price()
            self.commission_amount = commission.calculate_commission(self.total_price)


    """ Computed fields """
    @api.depends('stock_move_ids')
    def _compute_movement_count(self):
        for line in self:
            line.stock_move_count = len(line.stock_move_ids)

    @api.depends('total_price', 'commission_amount')
    def _compute_to_pay_amount(self):
        for line in self:
            line.to_pay_amount = line.total_price - line.commission_amount

    @api.depends('stock_move_ids.move_line_ids')
    def _compute_tracking_count(self):
        for line in self:
            line.stock_tracking_count = len(line.stock_move_ids.mapped('move_line_ids'))

    @api.depends('stock_move_ids.picking_id')
    def _compute_picking_ids(self):
        for line in self:
            line.picking_ids = line.stock_move_ids.mapped('picking_id')


    @api.depends('quantity', 'returned_quantity', 'unit_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.unit_price * line.remaining_quantity if line.remaining_quantity > 0 else 0

    @api.depends('quantity', 'returned_quantity')
    def _compute_remaining_quantity(self):
        for line in self:
            line.remaining_quantity = line.quantity - line.returned_quantity

    """ Methods """
    def _get_or_create_commission(self):
        """Find or create a commission record for the current product and partner."""
        self.ensure_one()
        Commission = self.env['consigned.commission']
        
        commission = Commission.search([
            ('product_id', '=', self.product_id.id), 
            ('partner_id', '=', self.partner_id.id)
        ], limit=1)

        if not commission:
            try:
                commission = Commission.create({
                    'product_id': self.product_id.id,
                    'partner_id': self.partner_id.id,
                    'commission_type': self.product_id.consigned_default_commission_type,
                    'commission_value': self.product_id.consigned_default_commission_value
                })
            except Exception as e:
                # Log error but don't interrupt the UI flow
                _logger.exception("Failed to create default commission: %s", e)
        return commission

    def _recalculate_commission(self):
        """Recalculate the commission for the current line."""
        self.ensure_one()
        self.commission_amount = self._get_or_create_commission().calculate_commission(self.total_price)

    """ Actions """

    def _action_add_partner_stock(self):
        for line in self:
            # check if the partner is already in the stock.location table
            partner_location = self.env['stock.location'].search([('name', '=', line.partner_id.name), ('location_id', '=', line.order_id.warehouse_id.partner_id.id)])
            if not partner_location:
                # create a new stock.location
                self.env['stock.location'].create({
                    'name': line.partner_id.name,
                    'location_id': line.order_id.warehouse_id.partner_id.id})
                


    def action_view_moves(self):
        self.ensure_one()
        return {
            'name': 'Stock Moves',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.stock_move_ids.ids)],
        }

    def action_view_pickings(self):
        self.ensure_one()
        return {
            'name': 'Transfers',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.picking_ids.ids)],
        }
        

