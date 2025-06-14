from odoo import _, api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

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
        ('canceled', 'Canceled')
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
    total_area = fields.Float(
        compute='_compute_total_area',
        string='Total Area (sqm)',
        help='Total area of the property including living area and garden'
    )
    best_offer = fields.Float(
        compute='_compute_best_price',
        string='Best Offer',
        help='Best offer made on the property'
    )

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = sum(
                filter(None, [record.living_area, record.garden_area])
            )

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = None
            self.garden_orientation = None
        elif self.garden and not self.garden_area:
            self.garden_area = 10  # Default garden area if not specified
            self.garden_orientation = 'north'  # Default orientation if not specified
            return {
                'warning': {
                    'title': _("Warning"),
                    'message': 'Default garden area set to 10 sqm and orientation set to North.'
                }
            }

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("You can't sell a canceled property"))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("You can't cancel a sold property"))
            record.state = 'canceled'
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_expected_price(self):
        precision=2
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=precision):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision) < 0:
                    raise ValidationError(_("The selling price should be at least 90% of the expected price."))