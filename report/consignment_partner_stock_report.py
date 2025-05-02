# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
import logging
from collections import defaultdict

_logger = logging.getLogger(__name__)


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
        - state: Optional filter for consignment order state
        
        Args:
            docids: The IDs of the records being printed
            data: A dictionary containing filter parameters from the wizard
                - settlement_date: Date to filter by (required)
                - partner_ids: List of partner IDs to filter (optional)
                - product_ids: List of product IDs to filter (optional)
                - state: State of consignment orders to filter (optional)

        Returns:
            dict: Values for the report template
        """

        # Build domain
        domain = [('settlement_date', '=', data['settlement_date'])]
        
        # Add optional filters
        if data.get('partner_ids'):
            domain.append(('partner_id', 'in', data['partner_ids']))
        if data.get('product_ids'):
            domain.append(('product_id', 'in', data['product_ids']))
        if data.get('state'):
            domain.append(('state', '=', data['state']))

        # Get order lines
        order_lines = self.env['consigned.order.line'].search(domain)

        # Group by partner
        partner_data = defaultdict(lambda: {'products': defaultdict(list), 'total_paid': 0})

        for line in order_lines:
            # Add line to products grouped by product_id
            partner_data[line.partner_id]['products'][line.product_id].append({
                'id': line.id,
                'product': line.product_id.name,
                'price': line.unit_price,
                'remaining': line.remaining_quantity,
                'returned': line.returned_quantity,
                'to_pay': line.total_price,
                'paid': 0,  # Assuming paid is a status to be determined by business logic
            })
            
            # Update totals
            # Placeholder for actual paid calculation based on business logic
            paid_amount = 0  # This should be calculated based on your business rules
            partner_data[line.partner_id]['total_paid'] += paid_amount

        # Convert to list for the template
        partners = []
        for partner, partner_data in partner_data.items():
            partner_info = {
                'partner': partner,
                'product_groups': [],
                'total_paid': partner_data['total_paid']
            }
            
            for product, lines in partner_data['products'].items():
                partner_info['product_groups'].append({
                    'product': product,
                    'lines': lines
                })
                
            partners.append(partner_info)

        # Return the data for the template
        return {
            'doc_ids': docids,
            'doc_model': 'consigned.order.line',
            'docs': order_lines,
            'settlement_date': data.get('settlement_date'),
            'partners': partners,
            'report_date': fields.Date.today(),
        }

