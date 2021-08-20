""" Initialize Work Center Question """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class WorkCenterQuestion(models.Model):
    """
        Initialize Work Center Question:
         - 
    """
    _name = 'work.center.question'
    _description = 'Work Center Question'
    _check_company_auto = True

    name = fields.Char(
        string='Question', required=True, translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
    )
    question_type = fields.Selection(
        [('free_text', 'Multiple Lines Text Box'),
         ('textbox', 'Single Line Text Box'),
         ('numerical_box', 'Numerical Value'),
         ('date', 'Date'),
         ('datetime', 'Datetime'),
         ('simple_choice', 'Multiple choice: only one answer'),
         ('multiple_choice', 'Multiple choice: multiple answers allowed'),
         ],
        default='free_text'
    )
    answer_choice_ids = fields.One2many(
        'answer.choice',
        'work_center_question_id'
    )
    work_center_type_id = fields.Many2one(
        'work.center.type'
    )


class OptionsChoice(models.Model):
    """
        Initialize Answer Choice:
         - 
    """
    _name = 'answer.choice'
    _description = 'Answer Choice'
    _rec_name = 'value'
    _check_company_auto = True

    value = fields.Char(
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
    work_center_question_id = fields.Many2one(
        'work.center.question'
    )
    is_correct = fields.Boolean(string='Is a correct answer')
