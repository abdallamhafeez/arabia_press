# -*- encoding: utf-8 -*-
##############################################################################
#
# Bista Solutions Pvt. Ltd
# Copyright (C) 2019 (http://www.bistasolutions.com)
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare, float_round


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'

    next_workorder_qty = fields.Float('Actual Output QTY',
                                      digits='Product Unit of Measure')
    currently_qty_produced = fields.Float('Currently Production Quantity',
                                          digits='Product Unit of Measure',
                                          readonly=True, default=0.0)

    @api.model
    def create(self, vals):
        res = super(MrpProductionWorkcenterLine, self).create(vals)
        res.next_workorder_qty = res.production_id.product_qty
        return res

    def record_production(self):
        """
            Override method to
        """
        if float_compare(self.next_workorder_qty, 0,
                         precision_rounding=self.product_uom_id.rounding) <= 0:
            raise UserError(_('Please set the Actual Output quantity need to'
                              ' be produce. It should be greater than zero.'))
        if self.next_workorder_qty > 0:
            if float_compare(
                    self.next_workorder_qty, 0,
                    precision_rounding=self.product_uom_id.rounding) <= 0:
                raise UserError(_('Please set the new product quantity needs to'
                                  ' be produce. It should be different'
                                  ' from zero.'))
        if self.next_workorder_qty and self.next_workorder_qty > self.qty_remaining:
            raise ValidationError(_(
                "New product quantity can not be greater than remaining quantity."))
        if not self.next_work_order_id and self.next_workorder_qty:
            self.qty_producing = self.next_workorder_qty or self.qty_producing
            self.currently_qty_produced = self.next_workorder_qty or self.qty_producing
        if self.currently_qty_produced > 0:
            if float_compare(self.qty_producing, 0,
                    precision_rounding=self.product_uom_id.rounding) <= 0:
                raise UserError(_('Please set the quantity you are currently'
                                  ' producing. It should be different'
                                  ' from zero.'))
            # If last work order, then post lots used
            if not self.next_work_order_id:
                self._update_finished_move()

            # Transfer quantities from temporary to final move line
            # or make them final
            self._update_moves()

            # Transfer lot (if present) and quantity produced to a
            # finished workorder line
            if self.product_tracking != 'none':
                self._create_or_update_finished_line()

            # Update workorder quantity produced
            self.qty_produced += self.qty_producing

            # Suggest a finished lot on the next workorder
            if self.next_work_order_id and self.production_id.product_id.\
                tracking != 'none' and not self.next_work_order_id.\
                    finished_lot_id:
                self.next_work_order_id.\
                    _defaults_from_finished_workorder_line(
                        self.finished_workorder_line_ids)
                # As we may have changed the quantity
                # to produce on the next workorder,
                # make sure to update its wokorder lines
                self.next_work_order_id._apply_update_workorder_lines()

            # One a piece is produced, you can launch the next work order
            self._start_nextworkorder()
            # Test if the production is done
            rounding = self.production_id.product_uom_id.rounding
            if float_compare(self.qty_produced, self.currently_qty_produced,
                             precision_rounding=rounding) < 0:
                previous_wo = self.env['mrp.workorder']
                if self.product_tracking != 'none':
                    previous_wo = self.env['mrp.workorder'].search([
                        ('next_work_order_id', '=', self.id)
                    ])
                candidate_found_in_previous_wo = False
                if previous_wo:
                    candidate_found_in_previous_wo = self.\
                        _defaults_from_finished_workorder_line(
                            previous_wo.finished_workorder_line_ids)
                if not candidate_found_in_previous_wo:
                    # self is the first workorder
                    self.qty_producing = self.qty_remaining
                    self.finished_lot_id = False
                    if self.product_tracking == 'serial':
                        self.qty_producing = 1

                self._apply_update_workorder_lines()
            else:
                self.qty_producing = 0
                self.button_finish()
            if not self.next_work_order_id:
                self.production_id.state = 'to_close'
            return True
        else:
            return super(MrpProductionWorkcenterLine, self).record_production()

    @api.depends('qty_production', 'qty_produced')
    def _compute_qty_remaining(self):
        for wo in self:
            if wo.currently_qty_produced > 0:
                wo.qty_remaining = float_round(
                    wo.currently_qty_produced - wo.qty_produced,
                    precision_rounding=wo.production_id.product_uom_id.rounding)
            else:
                return super(MrpProductionWorkcenterLine, self)._compute_qty_remaining()


    def _start_nextworkorder(self):
        rounding = self.product_id.uom_id.rounding
        if self.currently_qty_produced > 0 or self.next_workorder_qty != self.production_id.product_qty:
            if self.next_work_order_id.state == 'pending' and (
                    (self.operation_id.batch == 'no' and
                     float_compare(self.currently_qty_produced,
                                   self.qty_produced,
                                   precision_rounding=rounding) <= 0) or
                    (self.operation_id.batch == 'yes' and
                     float_compare(self.operation_id.batch_size,
                                   self.qty_produced,
                                   precision_rounding=rounding) <= 0)):
                self.next_work_order_id.update({
                    'state': 'ready',
                    'qty_producing': self.next_workorder_qty or self.qty_produced,
                    'currently_qty_produced':
                        self.next_workorder_qty or self.qty_produced,
                    'next_workorder_qty':
                        self.next_workorder_qty or 0.0
                    })
            elif self.next_workorder_qty > 0:
                self.next_work_order_id.update({
                    'state': 'ready',
                    'qty_producing': self.next_workorder_qty or self.qty_produced,
                    'currently_qty_produced':
                        self.next_workorder_qty or self.qty_produced,
                    'next_workorder_qty':
                        self.next_workorder_qty or 0.0,
                })
        else:
            return super(MrpProductionWorkcenterLine, self)._start_nextworkorder()

