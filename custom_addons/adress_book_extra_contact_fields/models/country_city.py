# -*- coding: utf-8 -*-
from openerp import models, fields, api, osv


class CountryCity(osv.osv):
    _description = "Country city"
    _name = "country.city"
    _columns = {
        "country_id": fields.Many2one("res.country", "Country",
                                      required=True),
        'state_id': fields.Many2one('res.country.state', 'State', required = True),
        'name': fields.Char('City Name', required=True,
                            help = 'Places in the country'),
    }
    _order = 'name'
