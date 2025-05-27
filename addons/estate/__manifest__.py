{
    'name': "Real Estate Management",
    'version': '1.0',
    'category': 'Real Estate',
    'depends': [
        'base'
        ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'summary': 'Manage real estate properties, listings, and transactions',
    'description': """
        This module provides functionalities to manage real estate properties, including listings, transactions, and client interactions.
    """,
    'author': 'Syamban',
    'installable': True,
    'application': True,
}