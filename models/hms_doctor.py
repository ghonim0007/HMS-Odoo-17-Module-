from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Full Name', compute='_compute_name', store=True)
    image = fields.Binary(string='Image') 
    department_id = fields.Many2one('hms.department', string='Department')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            if record.first_name and record.last_name:
                record.name = f"{record.first_name} {record.last_name}"
            elif record.first_name:
                record.name = record.first_name
            elif record.last_name:
                record.name = record.last_name
            else:
                record.name = "Doctor"

    def name_get(self):
        result = []
        for record in self:
            if record.first_name and record.last_name:
                name = f"Dr. {record.first_name} {record.last_name}"
            elif record.first_name:
                name = f"Dr. {record.first_name}"
            else:
                name = f"Doctor #{record.id}"
            result.append((record.id, name))
        return result