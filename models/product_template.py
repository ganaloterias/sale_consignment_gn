# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _check_company_auto = True

    can_be_consigned = fields.Boolean(string='Can be Consigned', default=False,
                                    help='Check this if the product can be used in consignment operations')

    consigned_default_commission = fields.Float(
        string='Consigned Default Commission',
        default=0.0,
        help='Default commission for consigned products'
    )


