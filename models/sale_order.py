# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    """ The class is used for inheriting sale order"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """the function to create a purchase order
        when conform sale order"""
        result = super(SaleOrder, self).action_confirm()
        for record in self.order_line:
            purchase_order = self.env['purchase.order'].create(
                {
                    'partner_id': record.product_template_id.seller_ids[
                        0].partner_id.id
                    if record.product_template_id.seller_ids else False
                    ,
                    'origin': self.name
                })
            purchase_order.update({
                "order_line": [(fields.Command.create({
                    "product_id": record.product_id.id,
                    "product_qty": record.product_uom_qty,
                    "price_unit": record.price_unit

                }))]
            })
        return result
