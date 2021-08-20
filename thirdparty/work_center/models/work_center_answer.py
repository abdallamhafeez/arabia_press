""" Initialize Workcenter Answer """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class WorkCenterAnswer(models.Model):
    """
        Initialize Work Center Answer:
         -
    """
    _name = 'work.center.answer'
    _description = 'Work Center Answer'
    _check_company_auto = True

    name = fields.Char(
        required=True, store=1,
        translate=True,
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

    textbox = fields.Char()
    free_text = fields.Text()
    numerical_box = fields.Integer()
    date = fields.Date()
    datetime = fields.Datetime()
    choice_ids = fields.Many2many(
        'answer.choice', 'choice_ids'
    )
    answer_choice_ids = fields.Many2many(
        'answer.choice', domain="[('id', 'in', choice_ids)]"
    )
    answer_choice_id = fields.Many2one(
        'answer.choice', domain="[('id', 'in', choice_ids)]"
    )

    mrp_routing_workcenter_id = fields.Many2one(
        'mrp.routing.workcenter'
    )
    answer = fields.Text()

    @api.onchange('free_text', 'textbox', 'numerical_box', 'date', 'datetime',
                  'answer_choice_ids', 'answer_choice_id')
    def _set_answer(self):
        """ Set Answer """
        if self.question_type == 'free_text':
            self.answer = self.free_text
        elif self.question_type == 'textbox':
            self.answer = self.textbox
        elif self.question_type == 'numerical_box':
            self.answer = str(self.numerical_box)
        elif self.question_type == 'date':
            self.answer = fields.Datetime.to_string(self.date)
        elif self.question_type == 'datetime':
            self.answer = fields.Datetime.to_string(self.datetime)
        elif self.question_type == 'simple_choice':
            self.answer = self.answer_choice_id.value
        else:
            answer = ""
            for rec in self.answer_choice_ids:
                answer += rec.value + ' '
            self.answer = answer
