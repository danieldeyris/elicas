odoo.define('quick_quotation.QuickOrderBarcodeHandler', function (require) {
"use strict";

var field_registry = require('web.field_registry');
var AbstractField = require('web.AbstractField');
var FormController = require('web.FormController');

FormController.include({

    _barcodeSelectedCandidate: function (candidate, record, barcode, activeBarcode, quantity) {
        var changes = {};
        var candidateChanges = {};
        candidateChanges[activeBarcode.quantity] = quantity ? candidate.data[activeBarcode.quantity] + quantity - 1: candidate.data[activeBarcode.quantity] + 1;
        changes[activeBarcode.fieldName] = {
            operation: 'UPDATE',
            id: candidate.id,
            data: candidateChanges,
        };
        return this.model.notifyChanges(this.handle, changes, {notifyChange: activeBarcode.notifyChange});
    },

});

var QuickOrderBarcodeHandler = AbstractField.extend({
    init: function() {
        this._super.apply(this, arguments);

        this.trigger_up('activeBarcode', {
            name: this.name,
            fieldName: 'order_line',
            quantity: 'product_uom_qty',
            setQuantityWithKeypress: true,
            notifyChange: true,
            commands: {
                    barcode: '_barcodeAddX2MQuantity',
            }
        });
    },
});

field_registry.add('quick_order_barcode_handler', QuickOrderBarcodeHandler);

});
