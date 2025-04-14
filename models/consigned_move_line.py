# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsignedMoveLine(models.Model):
    _name = 'consigned.move.line'
    _description = 'Consigned Move Line'

    move_id = fields.Many2one('consigned.move', string='Move', required=True, ondelete='cascade')
    lot_id = fields.Many2one('stock.production.lot', string='Lot/Serial Number')
    row = fields.Integer(string='Row Number') 