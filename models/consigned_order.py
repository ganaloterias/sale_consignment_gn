# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ConsignedOrder(models.Model):
    _name = 'consigned.order'
    _description = 'Consigned Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        tracking=True
    )
    settlement_date = fields.Date(
        string='Settlement Date',
        tracking=True
    )

    order_line_ids = fields.One2many(
        'consigned.order.line', 
        'order_id', 
        string='Order Lines'
    )

    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price'
    )
    
    movement_count = fields.Integer(
        string='Movement Count',
        compute='_compute_movement_count'
    )
    
    tracking_count = fields.Integer(
        string='Tracking Count',
        compute='_compute_tracking_count'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    picking_ids = fields.One2many('stock.picking', 'consignment_id', string='Transfers')
    picking_count = fields.Integer(string='Transfer Count', compute='_compute_picking_count')

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        default=lambda self: self.env['stock.warehouse'].search([], limit=1)
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    """ Computed fields """

    @api.depends('picking_ids')
    def _compute_picking_count(self):
        for order in self:
            order.picking_count = len(order.picking_ids)

    @api.depends('order_line_ids')
    def _compute_movement_count(self):
        for order in self:
            order.movement_count = sum(line.stock_move_count for line in order.order_line_ids)

    @api.depends('order_line_ids')
    def _compute_tracking_count(self):
        for order in self:
            order.tracking_count = sum(line.tracking_count for line in order.order_line_ids)

    @api.depends('order_line_ids')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(line.total_price for line in order.order_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                seq = self.env['ir.sequence'].next_by_code('consigned.order')
                if not seq:
                    seq = self.env['ir.sequence'].sudo().create({
                        'name': 'Consigned Order',
                        'code': 'consigned.order',
                        'prefix': 'CO/%(year)s/',
                        'padding': 5,
                    }).next_by_code('consigned.order')
                vals['name'] = seq
        return super(ConsignedOrder, self).create(vals_list) 
    
    """ Actions """
    
    def action_view_movements(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Movimientos',
            'res_model': 'consigned.order.line',
            'view_mode': 'list,form',
            'domain': [('order_id', '=', self.id)],
        }

    def action_view_pickings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfers',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.picking_ids.ids)],
        }

    def action_confirm(self):
        self.ensure_one()
        if not self.order_line_ids:
            raise UserError(_('Cannot confirm an order without lines.'))
        
        # Create outgoing picking
        picking_out = self._create_picking('outgoing')
        self.state = 'confirmed'
        return True

    def action_create_return(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Return'),
            'res_model': 'stock.return.picking',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.picking_ids[0].id if self.picking_ids else False},
        }

    def _create_picking(self, picking_type):
        self.ensure_one()
        if picking_type == 'outgoing':
            picking_type_id = self.warehouse_id.out_type_id
        else:
            picking_type_id = self.warehouse_id.in_type_id

        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type_id.id,
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            'consignment_id': self.id,
            'origin': self.name,
        })

        for line in self.order_line_ids:
            self.env['stock.move'].create({
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking_type_id.default_location_src_id.id,
                'location_dest_id': picking_type_id.default_location_dest_id.id,
                'consignment_line_id': line.id,
            })

        return picking

