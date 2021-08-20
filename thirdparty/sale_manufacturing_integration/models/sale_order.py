""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    production_request_ids = fields.One2many(
        'mrp.production.request', 'order_id'
    )
    requests_count = fields.Integer(compute='_compute_requests_count', store=1)

    @api.depends('production_request_ids')
    def _compute_requests_count(self):
        """ Compute requests_count value """
        for rec in self:
            rec.requests_count = len(rec.production_request_ids.ids)

    def new_production_request(self):
        """ :return Mrp Production Request action """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production.request',
            'name': _('Mrp Production Request'),
            'view_mode': 'form',
            'context': {'readonly': 1,
                        'default_order_id': self.id,
                        'default_partner_id': self.partner_id.id},
            'views': [(self.env.ref(
                'mrp_production_request.view_mrp_production_request_form').id,
                       'form')],
        }

    def action_view_mrp_production_request(self):
        """ :return Mrp Production Request action """
        self.ensure_one()
        recs = self.mapped('production_request_ids')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production.request',
            'name': _('Mrp Production Request'),
            'view_mode': 'tree,form',
            'context': {'readonly': 1,
                        'default_order_id': self.id,
                        'default_partner_id': self.partner_id.id},
            'domain': [('id', 'in', recs.ids)],
            'views': [(self.env.ref(
                'mrp_production_request.view_mrp_production_request_tree').id,
                       'tree'),
                      (self.env.ref(
                          'mrp_production_request.view_mrp_production_request_form').id,
                       'form')],
        }
