from odoo import fields, models, api


class PatientLog(models.TransientModel):
    _name = "log.wizard"
    _description = "Log Wizard"

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Char(
        "Created by", default=lambda self: self.env.user.name)
    date = fields.Date(default=fields.Date.today())
    description = fields.Text()

    def action_save_log(self):
        log = self.env['hms.patient.line'].create({
            'patient_id': self.patient_id.id,
            "description": self.description
        })
