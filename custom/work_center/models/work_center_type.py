""" Initialize Work Center Type """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class WorkCenterType(models.Model):
    """
        Initialize Work Center Type:
         - 
    """
    _name = 'work.center.type'
    _description = 'Work Center Type'
    _check_company_auto = True

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
    )
    work_center_question_ids = fields.One2many(
        'work.center.question', 'work_center_type_id'
    )
