{
    'name': 'Hospital Management System',
    'version': '1.1.0',
    'depends': ['base', 'crm'],
    'data': [
        "security/hms_security.xml",
        "security/ir.model.access.csv",
        "views/hms_patient_views.xml",
        "views/hms_patient_views_user.xml",
        "views/hms_doctor_views.xml",
        "views/hms_department_views.xml",
        "views/hms_menu_views_updated.xml",
        "views/res_partner_views.xml",
        "views/hms_patient_report.xml",
    ],
    'installable': True,
    'application': True,
}