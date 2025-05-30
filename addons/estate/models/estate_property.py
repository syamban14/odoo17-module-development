from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3), string='Available From')
    expected_price = fields.Float(required=True, string='Expected Price')
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean(default=False)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], default='new', string='Status')
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        required=True,
        ondelete='restrict'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
        ondelete='set null'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        ondelete='set null',
        copy=False
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags',
        help='Tags to categorize the property'
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        help='Offers made on the property'
    )