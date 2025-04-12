# -*- coding: utf-8 -*-
# from odoo import http


# class SaleConsignmentGn(http.Controller):
#     @http.route('/sale_consignment_gn/sale_consignment_gn', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_consignment_gn/sale_consignment_gn/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_consignment_gn.listing', {
#             'root': '/sale_consignment_gn/sale_consignment_gn',
#             'objects': http.request.env['sale_consignment_gn.sale_consignment_gn'].search([]),
#         })

#     @http.route('/sale_consignment_gn/sale_consignment_gn/objects/<model("sale_consignment_gn.sale_consignment_gn"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_consignment_gn.object', {
#             'object': obj
#         })

