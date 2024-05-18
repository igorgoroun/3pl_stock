{
    'name': "Third-party logistics stock management",
    'application': True,
    'version': '17.0.0.1',
    'depends': ['stock'],
    'author': "Ihor Horun",
    'category': 'Inventory/Inventory',
    'license': 'LGPL-3',
    'description': """
        Third-party logistics stock management.
        Qualification work of Ihor Horun, student of group number 4142
    """,
    'data': [
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/stock_picking_views.xml',
    ]
}
