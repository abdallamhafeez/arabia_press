""" Initialize Mrp Workcenter """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class MrpWorkcenter(models.Model):
    """
        Inherit Mrp Workcenter:
         -
    """
    _inherit = 'mrp.workcenter'

    work_center_type_id = fields.Many2one(
        'work.center.type'
    )
    work_center_question_ids = fields.One2many(
        related='work_center_type_id.work_center_question_ids'
    )
    other_cost = fields.Float()
