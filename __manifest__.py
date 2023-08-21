# -*- coding: utf-8 -*-
{
    'name': 'Customer Sale',
    'description': "Customer Sale",
    'category': 'Services',
    'version': '16.0.1.0.0',
    'author': 'Rasanath',
    'website': 'Cybrosys',
    'depends': ['base', 'sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/order_history_crone.xml',
        'views/customer_sale_order_view.xml',
        'views/product_product_view.xml',
        'views/sale_order_menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': True,
}
