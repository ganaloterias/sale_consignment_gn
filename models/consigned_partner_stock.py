# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConsignedPartnerStock(models.Model):
    _name = 'consigned.partner.stock'
    _description = 'Consigned Partner Stock'

    product_product_id = fields.Many2one('product.product', string='Product', required=True)
    product_template_id = fields.Many2one('product.template', string='Product Template', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    quantity = fields.Integer(string='Quantity', default=0)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
