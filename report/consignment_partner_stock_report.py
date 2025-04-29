# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class ConsignmentPartnerStockReport(models.AbstractModel):
    _name = 'report.sale_consignment_gn.consignment_partner_stock_report'
    _description = 'Consignment Partner Stock Report'

    def _get_report_values(self, docids, data=None):
        """
        Prepare the data for the consignment partner stock report.
        
        This report shows consigned order lines for each partner filtered by:
        - state: The status of the consignment order
        - settlement_date: The settlement date of the consignment order
        
        Args:
            docids: The partner IDs if specified, otherwise filter by data criteria
            data: A dictionary containing filter parameters
                - state: Status to filter (draft, pending, confirmed, done, cancel)
                - settlement_date: Date to filter by
        
        Returns:
            dict: Values for the report template
        """
        if not data:
            data = {}

        state = data.get('state')
        settlement_date = data.get('settlement_date')

        # If docids are provided, use them to get partners
        if docids:
            partner_ids = self.env['res.partner'].browse(docids)
        # Otherwise get all partners with consignment orders
        else:
            domain = []
            if state:
                domain.append(('state', '=', state))
            if settlement_date:
                domain.append(('settlement_date', '=', settlement_date))
            
            # Get all consignment orders that match the criteria
            orders = self.env['consigned.order'].search(domain)
            # Get unique partners from those orders
            partner_ids = orders.mapped('partner_id')

        # Prepare data for each partner
        docs = []
        for partner in partner_ids:
            # Get consignment orders for this partner
            domain = [('partner_id', '=', partner.id)]
            if state:
                domain.append(('state', '=', state))
            if settlement_date:
                domain.append(('settlement_date', '=', settlement_date))
            
            partner_orders = self.env['consigned.order'].search(domain)
            
            # Get all order lines from these orders
            order_lines = partner_orders.mapped('order_line_ids')
            
            if order_lines:
                docs.append({
                    'partner': partner,
                    'order_lines': order_lines,
                    'total_price': sum(line.total_price for line in order_lines)
                })

        return {
            'doc_ids': partner_ids.ids,
            'doc_model': 'res.partner',
            'docs': docs,
            'data': data,
        }

