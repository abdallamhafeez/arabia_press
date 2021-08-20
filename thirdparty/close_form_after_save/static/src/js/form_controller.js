odoo.define('close_form_after_save.FormController', function (require) {
    "use strict";

    let FormController = require('web.FormController');

    FormController.include({
        _onSave: function (ev) {
            if (this.initialState.context.save_close) {
                ev.stopPropagation(); // Prevent x2m lines to be auto-saved
                let self = this;
                this._disableButtons();
                this.saveRecord().then(this._enableButtons.bind(this)).guardedCatch(this._enableButtons.bind(this)).then(function () {
                    self.do_action({'type': 'ir.actions.act_window_close'})
                });
            } else {
                this._super.apply(this, arguments)
            }
        }
    })
})
