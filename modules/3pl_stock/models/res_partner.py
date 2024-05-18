import logging
from odoo import models, fields, api


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_location_id = fields.Many2one(comodel_name='stock.location', string='Main Location', required=False, ondelete='set null', )
    api_connected = fields.Boolean(string='API Connected', default=False, )
    api_login = fields.Char(string='API Login', required=False, )
    api_key = fields.Char(string='API Key', required=False, )

