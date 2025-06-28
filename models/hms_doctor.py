from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Image') 
    department_id = fields.Many2one('hms.department', string='Department')