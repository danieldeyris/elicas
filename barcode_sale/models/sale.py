# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        product = self.env['product.product'].search(
            ['|',('barcode', '=', barcode),('default_code', '=', barcode)]
            , limit=1)
        if product:
            order_lines = self.order_line.filtered(
                lambda r: r.product_id == product)
            if order_lines:
                order_line = order_lines[0]
                qty = order_line.product_uom_qty
                order_line.product_uom_qty = qty + 1
            else:
                newId = self.order_line.new({
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.lst_price
                })
                self.order_line += newId
                newId.product_id_change()
                return self._set_quantity()
        else:
            raise UserError(
                _('Scanned barcode %s is not related to any product.') %
                barcode)

    def _set_quantity(self):
        self.ensure_one()
        view_id = self.env.ref('barcode_sale.set_order_line_qty').id
        context = dict(
            self.env.context,
            order_line_id=self.id
        )
        return {
            'name': _('Quantité commandée'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'set.order.line.qty',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': context,
        }