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

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved_routing", "Approved Routing"),
            ("create_routing", "Create Routing"),
            ("done_routing", "Done Routing"),
            ("create_bom", "Create BOM"),
            ("done_bom", "Done BOM"),
            ("to_approve", "To Be Approved"),
            ("approved", "Approved"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        default="draft",
    )
    workcenter_ids = fields.Many2many(
        'mrp.workcenter', string='Work Center', readonly=True,
        states={'draft': [('readonly', False)]}
    )
    work_center_answer_ids = fields.One2many(
        'work.center.answer', 'mrp_production_request_id', readonly=True,
        states={'approved_routing': [('readonly', False)]}
    )
    workcenter_answer_line_ids = fields.Many2many(
        'workcenter.answer.line'
    )

    product_id = fields.Many2one(
        required=False, readonly=True,
    )
    bom_id = fields.Many2one(
        required=False, readonly=True
    )
    routing_name = fields.Char(
        readonly=True, states={'draft': [('readonly', False)]}
    )
    routing_id = fields.Many2one(
        'mrp.routing', readonly=True, states={'draft': [('readonly', False)]}
    )
    bom_product_temp_id = fields.Many2one(
        'product.template', 'Product',
        check_company=True,
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        readonly=True, states={'create_routing': [('readonly', False)],
                               'done_routing': [('readonly', False)]})
    bom_product_id = fields.Many2one(
        'product.product', 'Product Variant',
        check_company=True,
        domain="['&', ('product_tmpl_id', '=', bom_product_temp_id), ('type', 'in', ['product', 'consu']),  '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If a product variant is defined the BOM is available only for this product.",
        readonly=True, states={'create_routing': [('readonly', False)],
                               'done_routing': [('readonly', False)]},
        compute='_compute_bom_product', store=1
    )
    bom_product_qty = fields.Float(
        'Quantity', default=1.0,
        readonly=True, states={'create_routing': [('readonly', False)]})
    code = fields.Char(
        'Reference', readonly=True,
        states={'create_routing': [('readonly', False)],
                'done_routing': [('readonly', False)]})
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit')], 'BoM Type',
        default='normal', readonly=True,
        states={'create_routing': [('readonly', False)]})
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company,
        readonly=True, states={'create_routing': [('readonly', False)]}
    )
    ready_to_produce = fields.Selection([
        ('all_available', ' When all components are available'),
        ('asap', 'When components for 1st operation are available')],
        string='Manufacturing Readiness',
        default='asap',
        help="Defines when a Manufacturing Order is considered as ready to be started",
        required=True, readonly=True,
        states={'create_routing': [('readonly', False)]})
    consumption = fields.Selection([
        ('strict', 'Strict'),
        ('flexible', 'Flexible')],
        help="Defines if you can consume more or less components than the quantity defined on the BoM.",
        default='strict',
        string='Consumption',
        readonly=True, states={'create_routing': [('readonly', False)]}
    )
    product_uom_id = fields.Many2one(
        compute='_onchange_product_id', store=1
    )
    routing_options = fields.Selection(
        [('create', 'Create'),
         ('selection', 'Selection')
         ],
        default='create'
    )
    bom_option = fields.Selection(
        [('create', 'Create'),
         ('selection', 'Selection')
         ],
        default='create', string='BOM Options'
    )

    @api.depends('bom_product_temp_id')
    def _compute_bom_product(self):
        """ Compute bom_product_temp_id value """
        for rec in self:
            if rec.bom_product_temp_id:
                record = self.env['product.product'].search(
                    [('product_tmpl_id', '=', rec.bom_product_temp_id.id)],
                    limit=1)
                if record:
                    rec.bom_product_id = record.id

    def button_draft(self):
        self._check_reset_allowed()
        if self.bom_option == 'create':
            self.write({"state": "create_bom"})
        else:
            self.write({"state": "done_bom"})
        return True

    @api.depends("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id

    def create_bom(self):
        """ :return Mrp Bom action """
        if not self.bom_product_temp_id:
            raise ValidationError(_("Please Enter Product In BOM Page"))
        if not self.bom_product_id:
            raise ValidationError(_("Please Enter Product Variant In BOM Page"))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.bom',
            'name': _('Mrp Bom'),
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'create': False, 'save_close': True,
                'default_mrp_production_request_id': self.id,
                'default_routing_id': self.routing_id.id,
                'default_product_tmpl_id': self.bom_product_temp_id.id,
                'default_product_id': self.bom_product_id.id,
                'default_product_qty': self.bom_product_qty,
                'default_code': self.code,
                'default_type': self.type,
                'default_company_id': self.company_id.id,
                'default_ready_to_produce': self.ready_to_produce,
                'default_consumption': self.consumption,
            },
        }

    def delete_quest_answer(self):
        if self.work_center_answer_ids:
            for rec in self.work_center_answer_ids:
                self.work_center_answer_ids = [(2, rec.id)]

    def approved_routing(self):
        """ Approved Routing """
        if self.routing_options == 'create':
            if self.workcenter_ids:
                self.delete_quest_answer()
                work_center_answer_ids = []
                for work in self.workcenter_ids:
                    if work.work_center_question_ids:
                        for quest in work.work_center_question_ids:
                            work_center_answer_ids.append(
                                (0, 0, {'name': quest.name,
                                        'question_type': quest.question_type,
                                        'choice_ids': [
                                            (6, 0,
                                             quest.answer_choice_ids.ids)],
                                        'workcenter_id': work.id})
                            )
                if work_center_answer_ids:
                    self.work_center_answer_ids = work_center_answer_ids
        else:
            self.delete_quest_answer()
            if self.routing_id:
                work_center_answer_ids = []
                for operation in self.routing_id.operation_ids:
                    for quest in operation.work_center_answer_ids:
                        work_center_answer_ids.append((4, quest.id))
                if work_center_answer_ids:
                    self.work_center_answer_ids = work_center_answer_ids
        self.state = 'approved_routing'

    def create_routing(self):
        """ Create Routing """
        operation_ids = []
        for work in self.workcenter_ids:
            list_answer = []
            for answer in self.work_center_answer_ids:
                if answer.workcenter_id.id == work.id:
                    list_answer.append(answer.id)
            operation_ids.append(
                (0, 0, {'name': work.name, 'workcenter_id': work.id,
                        'work_center_answer_ids': [(6, 0, list_answer)]}))
        self.routing_id = self.env['mrp.routing'].create(
            {'name': self.routing_name, 'operation_ids': operation_ids})
        self.state = 'create_routing'

    def done_routing(self):
        """ Done Routing """
        self.state = 'done_routing'

    def action_view_mrp_routing(self):
        """ :return Mrp Routing action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.routing',
            'name': _('Mrp Routing'),
            'view_mode': 'form',
            'domain': [('id', '=', self.routing_id.id)],
            'res_id': self.routing_id.id,
            'views': [(self.env.ref('mrp.mrp_routing_form_view').id, 'form')],
        }

    def action_view_mrp_bom(self):
        """ :return Mrp Bom action """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.bom',
            'name': _('Mrp BOM'),
            'view_mode': 'form',
            'domain': [('id', '=', self.bom_id.id)],
            'res_id': self.bom_id.id,
            'views': [(self.env.ref('mrp.mrp_bom_form_view').id, 'form')],
        }

    def done_bom(self):
        """ Done Bom """
        if self.bom_id:
            self.state = 'done_bom'
        else:
            raise ValidationError(_("Please Enter Bill of Materials"))


class WorkCenterAnswer(models.Model):
    """
        Inherit Work Center Answer:
         -
    """
    _inherit = 'work.center.answer'

    mrp_production_request_id = fields.Many2one(
        'mrp.production.request'
    )
    workcenter_id = fields.Many2one(
        'mrp.workcenter'
    )


class WorkcenterAnswerLine(models.Model):
    """
        Initialize Workcenter Answer Line:
         -
    """
    _name = 'workcenter.answer.line'
    _description = 'Workcenter Answer Line'
    _check_company_auto = True

    workcenter_id = fields.Many2one(
        'mrp.workcenter'
    )
    work_center_answer_ids = fields.Many2many(
        'work.center.answer'
    )


class MrpBom(models.Model):
    """
        Inherit Mrp Bom:
         -
    """
    _inherit = 'mrp.bom'

    mrp_production_request_id = fields.Many2one(
        'mrp.production.request',
    )

    @api.model
    def create(self, vals_list):
        """ Override create """
        res = super(MrpBom, self).create(vals_list)
        if res.mrp_production_request_id:
            res.mrp_production_request_id.write(
                {'bom_id': res.id, 'state': 'create_bom',
                 'product_id': res.product_id.id})
        return res
