# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class ConsignmentPartnerStockReport(models.AbstractModel):
    _name = 'report.sale_consignment_gn.consignment_partner_stock_report'
    _description = 'Consignment Partner Stock Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Prepare the data for the consignment partner stock report.
        
        This report shows consigned order lines for each partner filtered by:
        - settlement_date: The settlement date of the consignment order (required)
        - partner_ids: Optional filter for specific partners
        - product_ids: Optional filter for specific products
        
        Args:
            docids: The IDs of the records being printed
            data: A dictionary containing filter parameters from the wizard
                - settlement_date: Date to filter by (required)
                - partner_ids: List of partner IDs to filter (optional)
                - product_ids: List of product IDs to filter (optional)
        
        Returns:
            dict: Values for the report template
        """
        
        if not data:
            data = {}
        
        print(data)
            
        # Get parameters from wizard
        settlement_date = data['settlement_date']
        partner_ids = data['partner_ids']
        product_ids = data['product_ids']
        
        if not settlement_date:
            settlement_date = fields.Date.today()
            
        # Build domain for consignment orders with given settlement date
        domain = [('settlement_date', '=', settlement_date)]
        
        # Get all consignment orders that match the criteria
        orders = self.env['consigned.order'].search(domain)
        
        # Filter partners if specified
        if partner_ids:
            orders = orders.filtered(lambda o: o.partner_id.id in partner_ids)
            
        # Get unique partners from filtered orders
        partners = orders.mapped('partner_id')
        
        # Prepare data for each partner
        docs = []
        for partner in partners:
            # Get order lines for this partner
            partner_orders = orders.filtered(lambda o: o.partner_id == partner)
            order_lines = partner_orders.mapped('order_line_ids')
            
            # Apply product filter if specified
            if product_ids:
                order_lines = order_lines.filtered(lambda l: l.product_id.id in product_ids)
            
            if order_lines:
                docs.append({
                    'partner': partner,
                    'order_lines': order_lines,
                    'total_price': sum(line.total_price for line in order_lines)
                })

        return {
            'doc_ids': docids.ids,
            'doc_model': 'consigned.order.line',
            'docs': docs,
            'data': data,
        }

