# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CreateLines(models.TransientModel):
    _name = 'create.line'

    @api.model
    def default_get(self, fields_list):
        pass
    #     defaults = super().default_get(fields_list)
    #     if 'order_line_id' in fields_list:
    #         order_line_id = self.env['quick.sale.order.line'].browse(defaults.get('order_line_id'))
    #     #defaults['product_uom_qty'] = 1
    #     return defaults
    #
    # order_line_id = fields.Many2one('quick.sale.order.line')
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', default=False)

    def set_qty(self):
        pass
    #     self.order_line_id.product_uom_qty += self.product_uom_qty
