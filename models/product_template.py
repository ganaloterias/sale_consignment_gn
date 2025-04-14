# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    can_be_consigned = fields.Boolean(string='Can be Consigned', default=False,
                                    help='Check this if the product can be used in consignment operations') 