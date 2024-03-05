from odoo import fields, models


class Task(models.Model):
    _name = 'todo.task'
    _description = 'Task'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    description = fields.Text()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ])
    file = fields.Binary()
