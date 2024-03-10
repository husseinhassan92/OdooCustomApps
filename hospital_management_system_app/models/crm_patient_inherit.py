from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CrmPatient(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    @api.model
    def create(self, vals_list):
        if "email" in vals_list:
            if self.env['hms.patient'].search([('email', '=', vals_list["email"])]):
                raise ValidationError("These Email Already Exists")
        return super().create(vals_list)

    def write(self, vals_list):
        if "email" in vals_list:
            if self.env['hms.patient'].search([('email', '=', vals_list["email"])]):
                raise ValidationError("These Email Already Exists")
        return super().write(vals_list)

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("These record can't be deleted")
        return super().unlink()
