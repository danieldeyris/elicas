# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare


class SetOrderLineQuantity(models.TransientModel):
    _name = 'set.order.line.qty'

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if 'order_line_id' in fields_list:
            order_line_id = self.env['sale.order.line'].browse(defaults.get('order_line_id'))
            defaults['product_uom_qty'] = order_line_id.product_uom_qty
        else:
            defaults['product_uom_qty'] = 1
        return defaults

    order_line_id = fields.Many2one('sale.order.line')
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)


    def set_qty(self):
        self.order_line_id.product_uom_qty = self.product_uom_qty

