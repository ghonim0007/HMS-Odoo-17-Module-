{
    'name': 'Hospital Management System',
    'depends': ['base', 'crm'],
    'data': [
        "views/hms_patient_views.xml",
        "views/hms_doctor_views.xml",
        "views/hms_department_views.xml",
        "views/hms_menu_views.xml",
        "views/res_partner_views.xml",
    ],
    'installable': True,
    'application': True,
}