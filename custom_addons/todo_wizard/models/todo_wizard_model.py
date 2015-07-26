# -*- coding utf-8 -*-

from openerp import models, fields, api
from openerp import exceptions

import logging
_logger = logging.getLogger(__name__)

class ToDoWizard(models.TransientModel):
    _name = "todo.wizard"
    task_ids = fields.Many2many("todo.task", string="Tasks")
    new_deadline = fields.Date("Deadline to Set")
    new_user_id = fields.Many2one("res.users", string="Responsible to set")

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise exceptions.ValidationError("No data to update!")
        # else:
        _logger.debug("Mass update on Todo Tasks %s", self.task_ids.ids)
        if self.new_deadline:
            self.task_ids.write({"date_deadline": self.new_deadline})
        if self.new_user_id:
            self.task_ids.write({"user_id": self.new_user_id})
        return True

