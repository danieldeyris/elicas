# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import _, models, fields, api
from odoo.exceptions import UserError


class QuickSaleOrder(models.Model):
    _name = 'quick.sale.order'
    _inherit = ['barcodes.barcode_events_mixin']
    _description = "Sales Order"
    _order = 'id desc'
    _check_company_auto = True

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('in_progress', 'En Cours'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, default='draft')
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    order_line = fields.One2many('quick.sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    last_product_id = fields.Many2one('product.product', string='Dernier article ajouté')

    nb_articles = fields.Float(string='Nombre articles', compute="_compute_nb_articles")

    def _compute_nb_articles(self):
        for order in self:
            order.nb_articles = sum(order.order_line.mapped('product_uom_qty'))

    def action_confirm_draft(self):
        if not self.partner_id:
            raise UserError(_('partner is mandatory.') )
        self.state = 'in_progress'

    def action_confirm(self):
        order_vals = {
            'partner_id': self.partner_id.id,
            'date_order': fields.Datetime.now(),
            'payment_term_id': self.partner_id.property_payment_term_id.id,
        }
        sale_order = self.env['sale.order'].create(order_vals)

        for line in self.order_line:
            sale_order_line = self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
            })

        sale_order.action_confirm()
        self.name = sale_order.name
        self.state = 'done'

    def on_barcode_scanned(self, barcode):
        product = self.env['product.product'].search(
            ['|',('barcode', '=', barcode),('default_code', '=', barcode)]
            , limit=1)
        if product:
            order_lines = self.order_line.filtered(lambda r: r.product_id == product)
            if order_lines:
                order_line = order_lines[0]
                qty = order_line.product_uom_qty
                order_line.product_uom_qty = qty + 1
            else:
                newId = self.order_line.new({
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'sequence': 0
                })
                self.order_line += newId
            self.last_product_id = product
        else:
            raise UserError(
                _('Scanned barcode %s is not related to any product.') %
                barcode)


class QuickSaleOrderLine(models.Model):
    _name = 'quick.sale.order.line'
    _description = 'Sales Order Line'
    _order = 'order_id, id desc'
    _check_company_auto = True

    order_id = fields.Many2one('quick.sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    sequence = fields.Integer(string='Sequence', default=10)

    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, readonly=True, index=True)
    product_barcode = fields.Char(related='product_id.barcode')

    price_unit = fields.Float(related='product_id.list_price')