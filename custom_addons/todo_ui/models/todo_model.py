# -*- codingL utf-8 -*-

from openerp import models, fields, api
from openerp.addons.base.res import res_request


def referencable_models(self):
    return res_request.referencable_models(self, self.env.cr, self.env.uid, context=self.env.context)


class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    # _parent_name = "parent_id"
    name = fields.Char("Name",size=40, translate=True)
    parent_id = fields.Many2one("todo.task.tag", "Parent Tag", ondelete="restrict")
    parent_left = fields.Integer("Parent left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many("todo.task.tag", "parent_id", "Child Tags")


class Stage(models.Model):
    _name = "todo.task.stage"
    _order = "sequence,name"
    # String fields:
    name = fields.Char("Name", size=40, translate=True)
    desc = fields.Text("Description")
    state = fields.Selection([('draft', 'New'), ('open', 'Started'), ('done', 'Closed')],'State')
    docs = fields.Html("Documentation")
    # Numeric fields:
    sequence = fields.Integer("Sequence")
    perc_complete = fields.Float("% Complete", (3,2))
    # Date fields:
    date_effective = fields.Date("Effective Date")
    date_changed = fields.Datetime("Last Changed")
    # Relational fields:
    todo_id = fields.One2many("todo.task", "stage_id", "Tasks in this stage")
    # Other fields:
    fold = fields.Boolean("Folded?")
    image = fields.Binary("Image")


class TodoTask(models.Model):
    _inherit = "todo.task"
    stage_id = fields.Many2one("todo.task.stage", "Stage")
    tag_ids = fields.Many2many("todo.task.tag", string="Tags")
    refers_to = fields.Reference(referencable_models, "Refers to")
    stage_fold = fields.Boolean("Stage Folded?", compute="_compute_stage_fold", search ="_search_stage_fold", inverse="_inverse_stage_fold")

    @api.one
    @api.depends
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return[("stage_id.fold", operator, value)]

    def _inverse_stage_fold(self):
        self.stage_id.fold = self.stage_fold