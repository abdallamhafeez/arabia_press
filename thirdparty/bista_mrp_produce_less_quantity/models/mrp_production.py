# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class mrp_production(models.Model):
    _inherit = 'mrp.production'

    actual_produced_qty = fields.Float(string='Actual Produced Quantity',
                                       digits='Product Unit of Measure',
                                       compute='_compute_actual_produced_qty')

    def _compute_actual_produced_qty(self):
        for production in self:
            actual_produced_qty = 0.00
            for workorder in production.workorder_ids:
                if not workorder.next_work_order_id:
                    actual_produced_qty = workorder.qty_produced

            production.actual_produced_qty = actual_produced_qty

    def action_reset_to_draft(self):
        '''
        This method makes mo to draft state.
        - creates return for transfer
        - delete components that are cancel
        - delete to be finish product move that are cancel
        - delete work-order / detail work order
        - and again creates component and all related move / detail work order.
        :return:
        '''
        self.create_transfer_return()
        self.move_raw_ids.sudo().filtered(lambda l: l.state == 'cancel').unlink()
        self.move_finished_ids.sudo().filtered(lambda l: l.state == 'cancel').unlink()
        self.workorder_ids.unlink()
        self.mrp_workorder_ids.unlink()
        qty = self.actual_produced_qty or self.product_qty
        self.onchange_product_id()
        self.state = 'draft'
        self._onchange_bom_id()
        self.product_qty = qty
        self._onchange_move_raw()
        self.onchange_routing_id()
