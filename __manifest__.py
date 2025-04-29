# -*- coding: utf-8 -*-
{
    'name': "Sale Consignment GN",

    'summary': "Manage consignment sales operations",

    'description': """
        This module adds consignment sales functionality:
        * Mark products as consignable
        * Track consigned inventory by partner
        * Manage consignment orders and movements
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'stock',
        'sale'
    ],

    # always loaded
    "data": [
        "data/sequence_data.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/consigned_commission_views.xml",
        "views/consigned_order_views.xml",
        "views/consigned_order_line_views.xml",
        "views/consigned_partner_stock.xml",
        "views/consigned_res_partner_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/consigned_report_wizard.xml",
        "report/consignment_order_reports.xml",
        "report/consignment_partner_stock_report.xml",
        "views/menu_views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}

