# -*- coding: utf-8 -*-
#
#
#    Author: Nicolas Bessi, Guewen Baconnier, Yannick Vaucher
#    Copyright 2013-2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
"""Adds a split button on stock picking out to enable partial picking without
   passing backorder state to done"""
from openerp import models, fields, api, _, exceptions



class stock_picking(models.Model):
    """Adds picking split without done state."""

    _inherit = "stock.picking"

    @api.multi
    def split_process(self):
        """Use to trigger the wizard from button with
           correct context"""
        ctx = {
            'active_model': self._name,
            'active_ids': self.ids,
            'active_id': len(self.ids) and self.ids[0] or False,
            'do_only_split': True,
            'default_picking_id': len(self.ids) and self.ids[0] or False,
        }
        view = self.env.ref('stock.view_stock_enter_transfer_details')
        return {
            'name': _('Enter quantities to split'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.transfer_details',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': ctx,
        }


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def split(self, move, qty,
              restrict_lot_id=False, restrict_partner_id=False):
        new_move_id = super(StockMove, self).split(
            move, qty,
            restrict_lot_id=restrict_lot_id,
            restrict_partner_id=restrict_partner_id,
        )
        new_move = self.browse(new_move_id)
        move_assigned = move.state == 'assigned'
        moves = move + new_move
        if move.reserved_availability > move.product_qty:
            moves.do_unreserve()
        if move_assigned:
            moves.action_assign()
        else:
            moves.action_confirm()
        if move.procurement_id:
            defaults = {'product_qty': qty,
                        'state': 'running'}
            new_procurement = move.procurement_id.copy(default=defaults)
            new_move.procurement_id = new_procurement
            move.procurement_id.product_qty = move.product_qty
        return new_move.id


class stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.v7
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(stock_transfer_details, self).default_get(cr, uid, fields, context=context)
        picking_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not picking_ids or len(picking_ids) != 1:
            # Partial Picking Processing may only be done for one picking at a time
            return res
        assert active_model in ('stock.picking'), 'Bad context propagation'
        picking_id, = picking_ids
        picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
        items = []
        packs = []
        if not picking.pack_operation_ids:
            picking.do_prepare_partial()
        for op in picking.pack_operation_ids:
            item = {
                'packop_id': op.id,
                'product_id': op.product_id.id,
                'product_uom_id': op.product_uom_id.id,
                'quantity': op.product_qty,
                'quantity_original': op.product_qty,
                'quantity_available': op.product_id.qty_available,
                'package_id': op.package_id.id,
                'lot_id': op.lot_id.id,
                'sourceloc_id': op.location_id.id,
                'destinationloc_id': op.location_dest_id.id,
                'result_package_id': op.result_package_id.id,
                'date': op.date,
                'owner_id': op.owner_id.id,
            }
            if op.product_id:
                items.append(item)
            elif op.package_id:
                packs.append(item)
        res.update(item_ids=items)
        res.update(packop_ids=packs)
        return res


class stock_transfer_details_items(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    @api.one
    @api.depends('quantity_available', 'quantity')
    def _validate_quantity(self):
        if self.quantity > self.quantity_available:
            raise exceptions.ValidationError("Quantity Should not be larger than quantity available.")
        return True

    quantity_available = fields.Float('Quantity Available', readonly=True)
    quantity_original = fields.Float('Quantity Original', default=1.0, readonly=True)
    validate_quantity = fields.Boolean('Validate Quality', compute='_validate_quantity', store=True, readonly=True)
