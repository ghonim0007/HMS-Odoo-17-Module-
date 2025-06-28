from odoo import models, fields, api
from odoo.exceptions import ValidationError
from lxml import etree
import json

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    STATES = [
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ]

    name = fields.Char(string='Patient Name')
    age = fields.Integer(string='Age')
    department_id = fields.Many2one(
        'hms.department',
        string="Department",
        domain=[('is_opened', '=', True)]
    )
    department_capacity = fields.Integer(
        related='department_id.capacity',
        string='Department Capacity'
    )
    doctor_ids = fields.Many2many(
        'hms.doctor',
        string='Doctors'
    )
    state = fields.Selection(
        STATES,
        string='State',
        default='undetermined'
    )
    log_history_ids = fields.One2many(
        'hms.log_history',
        'patient_id',
        string='Log History'
    )
    pcr = fields.Boolean(string='PCR')
    cr_ratio = fields.Float(string='CR Ratio')
    history = fields.Text(string='Medical History')

    @api.constrains('department_id')
    def _check_department_open(self):
        for record in self:
            if record.department_id and not record.department_id.is_opened:
                raise ValidationError("Cannot assign patient to a closed department!")

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked!")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Auto-checked",
                    'message': "PCR has been automatically checked for patients under 30.",
                }
            }

    @api.onchange('department_id')
    def _onchange_department(self):
        self.doctor_ids = [(5, 0, 0)]

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                new_state_label = dict(record._fields['state'].selection).get(vals['state'])
                self.env['hms.log_history'].create({
                    'patient_id': record.id,
                    'description': f"State changed to {new_state_label}",
                })
        return super(Patient, self).write(vals)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Patient, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if view_type == 'form':
            doc = etree.XML(res['arch'])

            if self.env.context.get('default_age', 0) < 50:
                history_field_nodes = doc.xpath("//field[@name='history']")
                for node in history_field_nodes:
                    # Mark the field as invisible
                    node.set('invisible', '1')
                    modifiers = json.loads(node.get("modifiers", '{}'))
                    modifiers['invisible'] = True
                    node.set("modifiers", json.dumps(modifiers))

            res['arch'] = etree.tostring(doc, encoding='unicode')

        return res
