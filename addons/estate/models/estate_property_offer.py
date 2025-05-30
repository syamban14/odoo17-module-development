from odoo import models, fields
class EstatePopertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(required=True, string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='accepted', string='Status')
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True,
        ondelete='cascade'
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
        ondelete='cascade'
    )