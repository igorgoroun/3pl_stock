from odoo import models, fields, api
from datetime import date, datetime
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    api_uuid = fields.Char(string='API Job ID', readonly=True, )
    partner_representative_name = fields.Char(string='Representative Name', readonly=False, )
    partner_representative_tel = fields.Char(string='Representative Contact Info', readonly=False, )

    @api.onchange('partner_id')
    def on_change_partner_id(self):
        self.owner_id = self.partner_id
        if self.partner_id.main_location_id:
            self.location_dest_id = self.partner_id.main_location_id

    def create_inbound_order(self, *args, uuid: str = None, partner_id: int = None, reference: str = None,
                             representative_name: str = None, representative_tel: str = None,
                             products: list = None, inbound_date: str = None):

        # format date
        if inbound_date is not None:
            inbound_date = datetime.strptime(inbound_date, '%Y-%m-%d')
        else:
            inbound_date = date.today()
        # check products existed in request
        if products is None or not products:
            raise ValueError('Products list is empty')
        # get partner and warehouse/locations objects
        partner = self.env['res.partner'].browse(partner_id)
        warehouse = self.env['stock.warehouse'].search([('code', '=', 'MAIN')], limit=1)
        src_location = self.env.ref('stock.stock_location_suppliers')
        dest_location = partner.main_location_id or warehouse.in_type_id.default_location_dest_id
        # create transfer
        inbound_transfer = self.create([{
            'api_uuid': uuid,
            'note': "API-created transfer with job uuid: {}".format(uuid),
            'partner_id': partner.id,
            'owner_id': partner.id,
            'partner_representative_name': representative_name,
            'partner_representative_tel': representative_tel,
            'origin': reference,
            'scheduled_date': inbound_date,
            'picking_type_id': warehouse.in_type_id.id,
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
            'move_ids': self.prepare_transfer_moves(products, partner.id, src_location.id, dest_location.id)
        }])
        _logger.info(f'Inbound order created: {inbound_transfer}')
        return True

    def prepare_transfer_moves(self, product_vals: list, partner_id: int, src_location_id: int, dest_location_id: int):
        move_lines = []
        for rec in product_vals:
            product = self.env['product.product'].get_or_create_product(rec, partner_id)
            move_lines.append((0, 0, {
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': rec.get('quantity', 0),
                'product_uom': self.env.ref('uom.product_uom_unit').id,
                'location_id': src_location_id,
                'location_dest_id': dest_location_id,
            }))
        return move_lines

    def issue_logistics_invoice(self):
        for rec in self:
            _logger.info(f'Computing invoicing data for {rec.name}')
        return True
