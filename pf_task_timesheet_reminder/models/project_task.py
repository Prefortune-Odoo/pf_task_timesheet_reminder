from odoo import models, api, fields

import logging
_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    last_reminder_datetime = fields.Datetime()
    last_notified_hours = fields.Float()
    last_timesheet_line_id = fields.Many2one(
        'account.analytic.line'
    )

    @api.model
    def send_timesheet_limit_reminder(self):
        
        template = self.env.ref(
            'pf_task_timesheet_reminder.timesheet_limit_reminder_email_template'
        )

        tasks = self.search([
            ('allocated_hours', '>', 0),
            ('effective_hours', '>', 0),
        ])

        for task in tasks:
            
            if task.effective_hours <= task.allocated_hours:
                continue

            latest_line = self.env['account.analytic.line'].search([
                ('task_id', '=', task.id)
            ], order='id desc', limit=1)

            if not latest_line:
                continue

            if (
                task.last_timesheet_line_id == latest_line
                and task.last_notified_hours == task.effective_hours
            ):
                continue

            assignee_emails = task.user_ids.mapped('partner_id.email')

            if not assignee_emails:
                continue

            email_values = {
                'email_to': ','.join(assignee_emails)
            }

            mail_id = template.with_context(
                      mail_notify_force_send=False,
                      default_notify=False,
                      mail_post_autofollow=False,
                      tracking_disable=True,
                    ).send_mail(
                      task.id,
                      force_send=True,
                      email_values={
                          'email_to': ','.join(assignee_emails),
                          'partner_ids': [],
                          'recipient_ids': [],
                      }
                    )

            task.write({
                'last_reminder_datetime': fields.Datetime.now(),
                'last_timesheet_line_id': latest_line.id,
                'last_notified_hours': task.effective_hours,
            })

        return True