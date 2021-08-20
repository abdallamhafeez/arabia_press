""" Initialize Mrp Production Request """

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, float_compare

from itertools import groupby


class MrpProductionRequest(models.Model):
    """
        Inherit Mrp Production Request:
         -
    """
    _inherit = 'mrp.production.request'

    order_id = fields.Many2one(
        'sale.order'
    )
    partner_id = fields.Many2one(
        'res.partner', string="Customer"
    )
    payment_term_id = fields.Many2one(
        related='partner_id.property_payment_term_id'
    )

    def new_quotations(self):
        """ :return Mrp Quotations  action """
        if self.partner_id:
            name = "[" + self.product_id.default_code + "]" if self.product_id.default_code else ""
            self.order_id = self.env['sale.order'].create(
                {'partner_id': self.partner_id.id, 'order_line': [
                    (0, 0, {'product_id': self.product_id.id,
                            'product_uom_qty': self.product_qty,
                            'price_unit': self.product_id.lst_price,
                            'name': name + self.product_id.name
                            }
                     )
                ]}).id
            return self.view_quotations()
        else:
            raise ValidationError(_('PLease Enter Customer'))

    def view_quotations(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'name': _('Quotation'),
            'view_mode': 'form',
            'context': {'create': False, 'partner_readonly': 1},
            'res_id': self.order_id.id,
            'views': [(self.env.ref('sale.view_order_form').id, 'form')],
        }
