from odoo import models, fields
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(required=True, string='Name')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Property type must be unique!'),
    ]