from odoo import models, api, fields

import logging
_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    last_reminder_datetime = fields.Datetime()
    last_notified_hours = fields.Float()

    @api.model
    def send_timesheet_limit_reminder(self):
        
        template = self.sudo().env.ref(
            'pf_task_timesheet_reminder.timesheet_limit_reminder_email_template'
        )

        tasks = self.sudo().search([
            ('planned_hours', '>', 0),
            ('effective_hours', '>', 0),
        ])

        for task in tasks:

            task._compute_effective_hours()
                        
            # condition: exceeded hours
            if task.effective_hours <= task.planned_hours:
                continue

            # 🔥 KEY LOGIC: detect NEW WORK added after last email
            new_hours_added = (
                task.effective_hours != task.last_notified_hours
            )

            if task.last_reminder_datetime and not new_hours_added:
                continue

            assignee_emails = task.user_ids.mapped('partner_id.email')

            if not assignee_emails:
                continue
            
            email_values = {
                'email_to': ','.join(assignee_emails)
            }
            
            template.sudo().send_mail(
                task.id,
                force_send=True,
                email_values=email_values
            )
            
            # update tracking
            task.last_reminder_datetime = fields.Datetime.now()
            task.last_notified_hours = task.effective_hours

        return True