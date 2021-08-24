""" Initialize Mrp Routing Workcenter """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, Warning


class MrpRoutingWorkcenter(models.Model):
    """
        Inherit Mrp Routing Workcenter:
         - 
    """
    _inherit = 'mrp.routing.workcenter'

    work_center_type_id = fields.Many2one(
        related='workcenter_id.work_center_type_id'
    )
    work_center_question_ids = fields.One2many(
        related='workcenter_id.work_center_question_ids', readonly=False
    )
    work_center_answer_ids = fields.One2many(
        'work.center.answer',
        'mrp_routing_workcenter_id'
    )

    @api.onchange('workcenter_id')
    def _onchange_workcenter_id(self):
        """ workcenter_id """
        if self.work_center_answer_ids:
            self.work_center_answer_ids = [(2, rec.id) for rec in
                                           self.work_center_answer_ids]
        else:
            work_center_answer_ids = []
            for quest in self.work_center_question_ids:
                work_center_answer_ids.append(
                    (0, 0, {'name': quest.name,
                            'question_type': quest.question_type,
                            'separate_in_report': quest.separate_in_report,
                            'choice_ids': [
                                (6, 0, quest.answer_choice_ids.ids)]})
                )
            self.work_center_answer_ids = work_center_answer_ids
