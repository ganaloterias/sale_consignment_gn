from odoo import models, fields, api, _

COMMISSION_TYPE = [
    ('percentage', 'Percentage'),
    ('fixed', 'Fixed')
]

class ConsignedCommission(models.Model):
    _name = 'consigned.commission'
    _description = 'Consigned Commission'
    _res_name = ['partner_id', 'product_id']


    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('can_be_consigned', '=', True)]", required=True)
    commission_type = fields.Selection(
        COMMISSION_TYPE,
        string='Commission Type',
        default='percentage',
        required=True
    )
    commission_value = fields.Float(
        string='Commission Value',
        default=0.0,
        required=True
    )
