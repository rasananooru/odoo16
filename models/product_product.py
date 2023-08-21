# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    """class to inherit product template"""
    _inherit = 'product.template'

    sale_count = fields.Integer(string="sale count",
                                compute='_compute_sale_count')

    def _compute_sale_count(self):
        """The function to compute sales count of a product"""
        for record in self:
            record.sale_count = sum(
                self.env['sale.order.line'].search(
                    [('product_template_id', '=', self.id)]).mapped(
                    'product_uom_qty'))

    @api.onchange('list_price')
    def _onchange_list_price(self):
        """The function to change the unit price when change sales price"""
        products = self.env['sale.order.line'].search([
            ('product_template_id', '=', self._origin.id),
            ('state', '=', 'draft')
        ])
        for product in products: product.price_unit = self.list_price
