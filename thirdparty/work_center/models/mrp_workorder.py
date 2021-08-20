""" Initialize Mrp Workorder """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class MrpWorkorder(models.Model):
    """
        Inherit Mrp Workorder:
         -
    """
    _inherit = 'mrp.workorder'

    work_center_type_id = fields.Many2one(
        related='workcenter_id.work_center_type_id'
    )

    work_center_answer_ids = fields.One2many(
        related='operation_id.work_center_answer_ids', readonly=False
    )
