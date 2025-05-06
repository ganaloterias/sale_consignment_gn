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
    
    """ A fin de centralizar la logica de calculo de comisiones, se crea un metodo que se encarga de calcular la comision
    de acuerdo al tipo de comision y el valor de la comision.
    
    Si llegase a existir una logica diferente para el calculo de comisiones, solo heredara este metodo.

    """
    def calculate_commission(self, amount):
        if self.commission_type == 'percentage':
            return amount * self.commission_value / 100
        else:
            return self.commission_value


""" Is also inherit from product.template to avoid creating a new field in the product.product model"""
class ConsignedProductTemplate(models.Model):
    _inherit = 'product.template'

    consigned_default_commission_type = fields.Selection(
        COMMISSION_TYPE,
        string='Consigned Default Commission Type',
        default='percentage',
    )

    consigned_default_commission_value = fields.Float(
        string='Consigned Default Commission Value',
        default=0.0,
    )