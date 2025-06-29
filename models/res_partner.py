from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
        help='Link this customer to a patient in the Hospital Management System'
    )

    vat = fields.Char(required=True, string='Tax ID')

    @api.constrains('related_patient_id')
    def _check_patient_email_unique(self):
        for record in self:
            if record.related_patient_id and record.related_patient_id.email:
                existing_customer = self.search([
                    ('email', '=', record.related_patient_id.email),
                    ('id', '!=', record.id)
                ])
                if existing_customer:
                    raise ValidationError(
                        f"Cannot link patient with email '{record.related_patient_id.email}' "
                        f"because this email is already assigned to customer: {existing_customer.name}"
                    )

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError(
                    f"Cannot delete customer '{record.name}' because it is linked to patient: {record.related_patient_id.name}. "
                    "Please unlink the patient first before deleting the customer."
                )
        return super(ResPartner, self).unlink()