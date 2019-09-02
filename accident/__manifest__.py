# -*- coding: utf-8 -*-
{
    'name': "accident",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['base'],
    'depends': ['mail'],
    'depends': ['project'],
    'depends': ['contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/HSE_USER_GROUPS.xml',
        'views/views.xml',
        'report/accident_report.xml',
        'report/accident_report_template.xml',
        'views/Accident.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
