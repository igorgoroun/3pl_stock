import json
import logging
import bcrypt
from passlib.context import CryptContext
from odoo import models, fields, api


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    main_location_id = fields.Many2one(comodel_name='stock.location', string='Main Location', required=False, ondelete='set null', )
    api_connected = fields.Boolean(string='API Connected', default=False, )
    api_login = fields.Char(string='API Login', required=False, )
    api_key = fields.Char(string='API Key', required=False, )

    def list_auth_data(self):
        auth_data = {}
        active_api_clients = self.search([
            ('active', '=', True),
            ('api_connected', '=', True),
            ('api_login', '!=', False),
            ('api_key', '!=', False)])
        if active_api_clients.exists():
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            for partner in active_api_clients:
                auth_data.update({
                    partner.api_login: {
                        'api_login': partner.api_login,
                        'api_key': pwd_context.hash(partner.api_key),
                        'partner_id': partner.id,
                    }
                })
        return auth_data
