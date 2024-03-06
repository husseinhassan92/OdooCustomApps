from odoo import fields, models


class Patient(models.Model):
    _name = "hms.patient"
    _description = "Patient"
    _rec_name = 'f_name'

    f_name = fields.Char("First Name")
    l_name = fields.Char("Last Name")
    b_date = fields.Date("Birth date")
    history = fields.Html("History")
    cr_ratio = fields.Float("CR Ratio")
    b_type = fields.Selection([
        ("o", "O"),
        ("a", "A"),
        ("b", "B"),
        ("ab", "AB")
    ], string="Blood Type")
    pcr = fields.Boolean("PCR")
    image = fields.Binary("Image")
    address = fields.Text("Address")
    age = fields.Integer("Age")
    department_id = fields.Many2one("hms.department")
    doctor_ids = fields.Many2many("hms.doctor")
