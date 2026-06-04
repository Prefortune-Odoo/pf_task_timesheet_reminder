# -*- coding: utf-8 -*-
{
    'name': "Task Timesheet Reminder",
    'version': '18.0.1.0.0',
    'category': 'services',
    'sequence': 10,
    'summary': " This module sends reminder emails when task timesheet hours exceed the allocated time. ",
    'license': 'OPL-1',
    'description': """ This module helps manage task timesheets by automatically sending reminder emails when logged hours exceed the allocated task time. It tracks timesheet entries in real time, detects updated or newly added hours, and helps maintain accurate task time management in Odoo. """,

    'author': "Prefortune Technologies LLP",
    'website': "https://www.prefortune.com/",
    'maintainer': 'Prefortune Technologies LLP',
    "support": "odoo@prefortune.com",
    'currency': 'EUR',
	'price': '0.00',
    'depends': [ 'project' , 'hr_timesheet'],
    'data': [
        
        'data/cron_task_timesheet_limit_mail_reminder_notification.xml',
        'views/timesheet_limit_reminder_mail_template.xml',
    
    ],
    "images": ["static/description/banner.png"],
    'installable' : True,
    'application': True,
    'auto_install' : False,

}
