# -*- coding: utf-8 -*-
{
    'name': "controle_equipement",

    'summary': """
        module de gestion et contrôles d'équipements ..""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/Equipement_VIEW.xml',
        'data/Equipement_sequence.xml',
        'views/Localisation_VIEW.xml',
        'views/categorie_VIEW.xml',
        'views/controles_view.xml',
        'data/Controle_sequence.xml',
        'views/alert_control_VIEW.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}