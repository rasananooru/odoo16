# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CustomerSale(models.Model):
    """ The class is used for inheriting res partner"""
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many(
        'sale.order', 'partner_id',
        readonly=True, help="sale orders")
    product_counts = fields.Integer(
        compute="_compute_product_count",
        help="product count")

    def action_view_product(self):
        """The function to view the products sold to a customer"""
        product_ids = self.env['sale.order.line'].search(
            [('order_partner_id', '=', self.id)]).product_id.mapped('id')
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'domain': [('id', 'in', product_ids)],
            'context': "{'create': False}"
        }

    def _compute_product_count(self):
        """Function to compute the total count of the
        product sold to a customer"""

        for record in self:
            product_count = tuple(self.env['sale.order.line'].search(
                [('order_partner_id', '=', self.id)]).product_id.mapped('id'))
            record.product_counts = len(product_count)
