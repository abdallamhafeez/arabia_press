# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning,UserError, ValidationError
    
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def delete_entry(self):
        for mv in self:
            mv.button_draft()
            mv.with_context(force_delete=True).unlink()
        return {
            'name': _('Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('account.view_move_tree').id, 'tree'), (False, 'form')],
        }

    def delete_entry_tree(self):
        for mv in self:
            mv.button_draft()
            mv.with_context(force_delete=True).unlink()
        return {
            'name': _('Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('account.view_move_tree').id, 'tree'), (False, 'form')],
        }
