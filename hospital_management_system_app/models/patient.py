import re
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "hms.patient"
    _description = "Patient"
    _rec_name = 'f_name'

    f_name = fields.Char("First Name", required=1)
    l_name = fields.Char("Last Name", required=1)
    b_date = fields.Date("Birth date")
    history = fields.Html("History")
    cr_ratio = fields.Float("CR Ratio")
    b_type = fields.Selection([
        ("o", "O"),
        ("a", "A"),
        ("b", "B"),
        ("ab", "AB")
    ], string="Blood Type")
    state = fields.Selection([
        ("undetermined", "Undetermined"),
        ("serious", "Serious"),
        ("fair", "Fair"),
        ("good", "Good")
    ], string="State")
    pcr = fields.Boolean("PCR")
    image = fields.Binary("Image")
    address = fields.Text("Address")
    email = fields.Char("Email")
    age = fields.Integer("Age", compute='compute_age')
    department_id = fields.Many2one("hms.department", string="Department")
    doctor_ids = fields.Many2many("hms.doctor", string="Doctors")
    line_ids = fields.One2many('hms.patient.line', 'patient_id')

    @api.onchange('age')
    def check_pcr(self):
        for rec in self:
            if rec.age < 30 and rec.age != 0:
                rec.pcr = True
                return {
                    'warning': {
                        'message': "PCR checked"
                    }
                }
            else:
                rec.pcr = False

    @api.model
    def create(self, vals_list):
        if "email" in vals_list:
            if self.search([('email', '=', vals_list["email"])]):
                raise ValidationError("These Email Already Exists")
            else:
                if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', vals_list["email"]):
                    raise ValidationError("These Email Is Invalid")
        return super().create(vals_list)

    def write(self, vals_list):
        if "email" in vals_list:
            if self.search([('email', '=', vals_list["email"])]):
                raise ValidationError("These Email Already Exists")
            else:
                if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', vals_list["email"]):
                    raise ValidationError("These Email Is Invalid")

        return super().write(vals_list)

    @api.depends('b_date')
    def compute_age(self):
        for rec in self:
            if rec.b_date:
                rec.age = relativedelta(fields.Date.today(), rec.b_date).years
            else:
                rec.age = False

    def action_add_log(self):
        print("book")
        action = self.env['ir.actions.actions']._for_xml_id(
            'hospital_management_system_app.log_wizard')
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action

    @api.onchange('state')
    def add_log(self):
        log = self.env['hms.patient.line'].create({
            "patient_id": self.id.origin,
            "description": f"State changed {self.state}"
        })

    def action_undetermined(self):
        for rec in self:
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.state = 'good'

    def action_fair(self):
        for rec in self:
            rec.state = 'fair'

    def action_serious(self):
        for rec in self:
            rec.state = 'serious'


class PatientLine(models.Model):
    _name = 'hms.patient.line'
    _description = 'Patient Line'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Char(
        "Created by", default=lambda self: self.env.user.name)
    date = fields.Date(default=fields.Date.today())
    description = fields.Text()
