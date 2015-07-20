from openerp import models, fields, osv


class InheritedResPartner(models.Model):
    _inherit = "res.partner"
    postal_street = fields.Char("Postal street")
    postal_street2 = fields.Char("Postal street 2")
    postal_zip = fields.Char("Postal zip")
    postal_city = fields.Many2one("country.city", "Postal city")
    postal_state_id = fields.Many2one("res.country.state", "Postal state")
    postal_country_id = fields.Many2one("res.country", "Postal country" )