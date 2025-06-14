from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True, string='Name')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Tag must be unique!'),
    ]