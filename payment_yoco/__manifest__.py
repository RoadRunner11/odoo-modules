# -*- coding: utf-8 -*-
{
    'name': "Yoco Payment Acquirer",

    'summary': """
        Payment Acquirer for Yoco Payments""",

    'description': """
        This module is created for clients that want to
        use Yoco Payments as the one of the payment gateways in 
        their Odoo system
    """,

    'author': "Fodilu Olawale Akorede",
    'website': "https://www.ehiotech.com/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/yoco_views.xml',
        'views/payment_yoco_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
