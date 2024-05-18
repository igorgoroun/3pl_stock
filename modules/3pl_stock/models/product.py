from odoo import models, fields, api, _
import logging


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    owner_id = fields.Many2one('res.partner', store=True, compute='_compute_owner_id', string=_('Належіть до'), required=False,)

    @api.depends('product_variant_ids', 'product_variant_id')
    def _compute_owner_id(self):
        for record in self:
            record.owner_id = record.product_variant_id.owner_id


class ProductProduct(models.Model):
    _inherit = 'product.product'

    owner_id = fields.Many2one('res.partner', string=_('Належіть до'), required=False, )

    _sql_constraints = [
        ('product_code_barcode_partner_combined_key', 'unique(default_code, barcode, owner_id)', 'Merge ID must be unique per MailChimp Lists!')
    ]

    def get_or_create_product(self, product_data: dict, partner_id: int):
        if not all([product_data.get('default_code', False), product_data.get('quantity', False)]):
            raise ValueError(f"Missing default code and quantity for product {product_data} ")
        product = self.search([
            ('default_code', '=', product_data.get('default_code')),
            ('owner_id', '=', partner_id),
        ], limit=1)
        if not product.exists():
            product = self.create([{
                'default_code': product_data.get('default_code'),
                'owner_id': partner_id,
                'type': 'product',
                'name': product_data.get('name'),
                'description': product_data.get('description'),
                'barcode': product_data.get('barcode'),
                'standard_price': product_data.get('price'),
                'list_price': product_data.get('price'),
            }])
        return product