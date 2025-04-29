# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ConsignedReportWizard(models.TransientModel):
    _name = 'consigned.report.wizard'
    _description = _('Consigned Report Wizard')
    _res_name = 'settlement_date'

    settlement_date = fields.Date(_('Settlement Date'), required=True)
    partner_ids = fields.Many2many('res.partner', string=_('Partner'))
    product_ids = fields.Many2many('product.product', string=_('Product'), domain="[('can_be_consigned', '=', True)]")

    def print_report(self):
        data = {
            'settlement_date': self.settlement_date,
            'state': 'confirmed',
            'partner_ids': self.partner_ids.ids if self.partner_ids else [],
            'product_ids': self.product_ids.ids if self.product_ids else [],
        }
        return self.env.ref('sale_consignment_gn.action_report_consignment_partner_stock').report_action(self, data)
