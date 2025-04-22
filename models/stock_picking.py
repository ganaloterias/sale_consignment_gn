# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    consignment_id = fields.Many2one('consigned.order', string='Consignment Order', copy=False)
    is_consignment = fields.Boolean(string='Is Consignment', compute='_compute_is_consignment', store=True)
    consignment_move_ids = fields.Many2many('stock.move', string='Consignment Moves', 
        compute='_compute_consignment_move_ids')

    @api.depends('consignment_id')
    def _compute_is_consignment(self):
        for picking in self:
            picking.is_consignment = bool(picking.consignment_id)

    @api.depends('consignment_id', 'move_ids.consignment_line_id')
    def _compute_consignment_move_ids(self):
        for picking in self:
            if not picking.consignment_id:
                picking.consignment_move_ids = False
                continue
            
            # Obtener las líneas de consignación relacionadas
            consignment_lines = picking.consignment_id.mapped('order_line_ids')
            # Obtener todos los movimientos relacionados con estas líneas
            related_moves = consignment_lines.mapped('stock_move_ids')
            # Filtrar los movimientos que no son del picking actual
            picking.consignment_move_ids = related_moves.filtered(lambda m: m.picking_id != picking) 