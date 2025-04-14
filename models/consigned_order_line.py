# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsignedOrderLine(models.Model):
    _name = 'consigned.order.line'
    _description = 'Consigned Order Line'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    order_id = fields.Many2one('consigned.order', string='Order', required=True, ondelete='cascade')
    quantity = fields.Integer(string='Quantity', required=True)
    returned_quantity = fields.Integer(string='Returned Quantity', default=0) 