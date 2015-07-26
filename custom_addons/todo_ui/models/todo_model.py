# -*- codingL utf-8 -*-
from django.utils import dateformat

from openerp import models, fields, api
from openerp.addons.base.res import res_request
from openerp.exceptions import ValidationError
from datetime import date, datetime, time

def referencable_models(self):
    return res_request.referencable_models(self, self.env.cr, self.env.uid, context=self.env.context)


class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    # _parent_name = "parent_id"
    name = fields.Char("Name", size=40, translate=True)
    parent_id = fields.Many2one("todo.task.tag", "Parent Tag", ondelete="restrict")
    parent_left = fields.Integer("Parent left", index=True)
    parent_right = fields.Integer("Parent Right", index=True)
    child_ids = fields.One2many("todo.task.tag", "parent_id", "Child Tags")
    _date_deadline_passed = False


class Stage(models.Model):
    _name = "todo.task.stage"
    _order = "sequence,name"
    # String fields:
    name = fields.Char("Name", size=40, translate=True)
    desc = fields.Text("Description")
    state = fields.Selection([('draft', 'New'), ('open', 'Started'), ('done', 'Closed')], 'State')
    docs = fields.Html("Documentation")
    # Numeric fields:
    sequence = fields.Integer("Sequence")
    perc_complete = fields.Float("% Complete", (3, 2))
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
    refers_to = fields.Reference(referencable_models, string="Refers to")
    stage_fold = fields.Boolean("Stage Folded?", compute="_compute_stage_fold", search="_search_stage_fold",
                                inverse="_inverse_stage_fold")
    stage_state = fields.Selection(related="stage_id.state", string="Stage State")
    _sql_constraints = [("todo_task_name_uniq", "UNIQUE (name, user_id, active)", "Task title must be unique!")]
    date_start = fields.Date("Start Date")


    @api.one
    @api.depends
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [("stage_id.fold", operator, value)]

    def _inverse_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    # check if the name of the task is longer then 5 characters
    @api.one
    @api.constrains("name")
    def _check_name_size(self):
        if len(self.name) < 5:
            raise ValidationError("Must have 5 chars!")

    # check if the start date is before the deadline
    @api.one
    @api.constrains("date_deadline","date_start")
    def _date_start_before_date_deadline(self):
        if self.date_start > self.date_deadline:
            raise ValidationError("The start date must be before the deadline!")

    # compute the amount of tasks for the user
    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count([("user_id", "=", self.user_id.id)])

    user_todo_count = fields.Integer("User To-Do Count", compute="compute_user_todo_count")

    # compute the days needed to complete a task
    # @api.one
    # def compute_effort_estimate(self):
    #     startdate = datetime.strptime(self.date_start., "%d")
    #     deadlinedate = datetime.strptime("self.date_deadline", "%d")
    #
    #
    #     self.effort_estimate = (deadlinedate - startdate).days
    #
    # effort_estimate = fields.Date("Effort Estimate (Days)", compute="compute_effort_estimate")

    # TODO effort_estimate automatisch laten berekenen als date_start en date_deadline zijn ingevuld.
    effort_estimate = fields.Integer("Effort estimate (Days)")
