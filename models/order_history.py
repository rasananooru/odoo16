# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models


class OrderHistory(models.Model):
    """ The class is used for creating model order history"""
    _name = 'order.history'
    _description = 'order history'
    _rec_name = 'sale_id'

    sale_id = fields.Many2one(
        "sale.order", string="Name",readonly=True)
    purchase_ids = fields.Many2many(
        "purchase.order",string="purchases", readonly=True)
    vendor_ids = fields.Many2many(
        "res.partner", string="Vendors", readonly=True)
    partner_id = fields.Many2one(
        "res.partner", string="customer",readonly=True)
    order_date = fields.Date(string="date", help="ordered date")
    sales_person_id = fields.Many2one(
        "res.users", string="Sales Person",
        help="sales person of the sale order",readonly=True)

    @api.model
    def _generate_order_history(self):
        """The function is used to generate order history"""
        order_history=self.search(
            []).mapped('sale_id').mapped('name')
        sales = self.env['sale.order'].search([('date_order', '>=',
                                                datetime.date.today()),
                                               ('state', '=', 'sale'),
                                               ('name','not in',order_history)])
        for record in sales:
            order_history = self.create({
                'sale_id': record.id,
                'partner_id': record.partner_id.id,
                'sales_person_id': record.user_id.id,
                'order_date': record.date_order
            })
            purchase_order = self.env['purchase.order'].search([
                ('origin', '=', record.name)
            ])
            for order in purchase_order:
                vendors = tuple(order.mapped('partner_id'))
                order_history.update({
                    'purchase_ids': [(
                        fields.Command.link(order.id)
                    )]
                })
                for vendor in vendors:
                    order_history.update({
                        'vendor_ids': [(
                            fields.Command.link(vendor.id)
                        )]
                    })
