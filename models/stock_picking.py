# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    consignment_id = fields.Many2one('consigned.order', string='Consignment Order', copy=False)
    is_consignment = fields.Boolean(string='Is Consignment', compute='_compute_is_consignment', store=True)

    @api.depends('consignment_id')
    def _compute_is_consignment(self):
        for picking in self:
            picking.is_consignment = bool(picking.consignment_id)

    # Cuando una orden sea confirmada ajusta el stock de ConsignedPartnerStock
    def action_confirm(self):
        super(StockPicking, self).action_confirm()
        if self.consignment_id:
            for picking in self:
                for move in picking.move_ids:
                    # Buscar el registro de ConsignedPartnerStock existente
                    consigned_partner_stock = self.env['consigned.partner.stock'].search([
                        ('product_product_id', '=', move.product_id.id),
                        ('partner_id', '=', self.consignment_id.partner_id.id)
                    ], limit=1)
                    
                    if consigned_partner_stock:
                        # Actualizar la cantidad existente
                        consigned_partner_stock.quantity += move.quantity
                    else:
                        # Crear un nuevo registro
                        self.env['consigned.partner.stock'].create({
                            'product_product_id': move.product_id.id,
                            'product_template_id': move.product_id.product_tmpl_id.id,
                            'quantity': move.quantity,
                            'partner_id': self.consignment_id.partner_id.id,
                        })
    

