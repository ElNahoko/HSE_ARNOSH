# -*- coding: utf-8 -*-
{
    'name': "Engin",

    'summary': """
        Sh, used as
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
    'depends': ['base', 'mail', 'mass_mailing'],

    # always loaded
    'data': [
        'security/HSE_USER_GROUPS.xml',
        'security/ir.model.access.csv',
        'report/report_action_engin.xml',
        'report/report_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/EnginV.xml',
        'views/ControlEng.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}