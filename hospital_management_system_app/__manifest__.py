{
    'name': "HMS App",
    'summary': """ """,
    'description': """ """,
    'author': "Hussein Hassan",
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': ['base',
                'crm',
                ],
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/patient.xml',
        'views/department.xml',
        'views/doctor.xml',
        'views/crm_patient_inherit.xml',
        'wizard/add_patient_log.xml',
        'report/patient_report.xml'
    ],
}
