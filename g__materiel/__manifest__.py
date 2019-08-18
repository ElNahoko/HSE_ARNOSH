# -*- coding: utf-8 -*-
{
    'name': "G_Materiel",

    'summary': """
        Gestion et maintenance de materiels internes """,

    'description': """
       Module de suivis et maintenance d'équipements
    """,

    'author': "Guedira",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','workflow'],

    # always loaded
    'data': [
        'data/Equipement_sequence.xml',
        'security/ir.model.access.csv',
        'views/maintenance_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}