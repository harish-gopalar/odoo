# -*- coding: utf-8 -*-
##############################################################################
#
#    JMR Infotech, Bank Along
#    Copyright © 2016. JMR Infotech All Rights Reserved.
#
#    With delivery and development centers in India,
#    sizable global presence and customers spread across 5 continents,
#    JMR Infotech is a leader in Information Technology solutions and services.
#    In our short existence, since 2007, we have grown to have top brands as our clients.
#
##############################################################################

from openerp import models, fields, api, exceptions
from datetime import datetime


class principal_departments(models.Model):
    _name = 'principal.departments'
    _description = 'Principal Departments'
    _order = "id desc"

    name = fields.Char('Principal Name', required=True)


class minutes_meeting(models.Model):
    _name = 'minutes.meeting'
    _description = 'Minutes of Meeting'
    _order = "id desc"
    _rec_name = 'date'

    date = fields.Date('Date', required=True, default=lambda self: fields.datetime.now())
    attendees = fields.Char('Attendees', required=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    description = fields.Text('Description', required=True)
    ref_id = fields.Many2one('principal.touch.point', 'Reference', readonly=True)


class sales_pipe_projection(models.Model):
    _name = 'sales.pipe.projection'
    _inherit = ['mail.thread']
    _description = 'Sales Pipe Projection'

    AVAILABLE_QUARTERS = [
        ('1', 'Q1'),
        ('2', 'Q2'),
        ('3', 'Q3'),
        ('4', 'Q4'),
    ]

    name = fields.Selection(AVAILABLE_QUARTERS, 'Quarter')
    department_id = fields.Many2one('hr.department', 'Business Unit')
    user_id = fields.Many2one('res.users', 'Field Salesperson')
    ob_target = fields.Float('Order Booking Target')
    actual_pipe = fields.Float('Pipe Actual')
    call_deals = fields.Float('Call Deals')
    focus_solutions = fields.Float('Focus Solutions')
    total_pipe = fields.Float('Total Pipe Value')
    remainder_pipe = fields.Float('Remainder of Pipe')
    upper_control = fields.Float('Pipe Upper Control Limit (10XOB)')
    lower_control = fields.Float('Pipe Lower Control Limit (5XOB)')