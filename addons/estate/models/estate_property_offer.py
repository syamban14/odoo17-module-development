from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError
class EstatePopertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(required=True, string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='', string='Status')
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
    validity = fields.Integer(
        default=7,
        string='Validity (days)',
        help='Number of days the offer is valid'
    )
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse ='_inverse_date_deadline',
        string='Deadline',
        store=True,
        help='Deadline for the offer based on validity'
    )

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
            # Calculate validity based on the difference between deadline and creation date
                offer.validity = (offer.date_deadline - offer.create_date.date()).days if offer.create_date else 0
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError('The property is already sold')
            offer.status = 'accepted'
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'