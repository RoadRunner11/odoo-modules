{
    'name': "Manufacturing",

    'summary': """
        Manufacturing Resource Planning with setup of materials and specifications, procurement and inventory management""",

    'description': """
       Manufacturing Resource Planning with setup of materials and specifications, procurement and inventory andmanagement
    """,

    'author': "Ehio Technologies",
    'website': "https://www.ehiotech.com",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/setup/materials_views.xml',
        'views/setup/storage_conditions_views.xml',
        'views/setup/tests_views.xml',
        'views/setup/specifications_views.xml',
        'views/inventory/requisitions_views.xml',
        'views/inventory/pending_receipts_views.xml',
        'views/inventory/inventory_views.xml',
        'views/project/project_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False
}
