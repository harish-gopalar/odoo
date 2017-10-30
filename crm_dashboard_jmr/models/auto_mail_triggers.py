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

from openerp import models, fields, api, _
import datetime


class hr_department(models.Model):
    _inherit = 'hr.department'

    target = fields.Float('BU Target')


class bu_lead_achieved(models.Model):
    _name = 'bu.leads.achieved'
    _description = 'BU Leads Achieved'
    _order = "id desc"

    lead_id = fields.Many2one('crm.lead', 'Lead')
    currency_id = fields.Many2one('res.currency', 'Currency ID', related="lead_id.currency_id", store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer Name', related="lead_id.partner_id", store=True, readonly=True)
    user_id = fields.Many2one('res.users', 'Fields SalesPerson', related="lead_id.user_id", store=True, readonly=True)
    name = fields.Char('Opportunity Name', related="lead_id.name", store=True, readonly=True)
    closed_won_date = fields.Date('Close/won date', related="lead_id.closed_won_date", store=True, readonly=True)
    planned_revenue = fields.Float('Expected Revenue', related="lead_id.planned_revenue", store=True, readonly=True)
    department_id = fields.Many2one('hr.department', 'Business Unit', related="lead_id.department_id", store=True,
                                    readonly=True)
    department_product_ids = fields.Many2many('department.product', 'bu_achievements_department_product',
                                              'lead_id', 'department_product_id', 'Product/Interest Area',
                                              related="lead_id.department_product_ids", readonly=True)
    ref_id = fields.Many2one('bu.achievement', 'Reference', readonly=True)


class bu_achievement(models.Model):
    _name = 'bu.achievement'
    _inherit = ['mail.thread']
    _description = 'BU Achievement'
    _order = "id desc"
    _rec_name = "department_id"

    @api.one
    @api.depends('revenue_achieved', 'target', )
    def _compute_percentage(self):
        if self.target:
            self.percentage = round(float(self.revenue_achieved) * 100 / self.target, 2)
        else:
            self.mapped_percentage = 0

    department_id = fields.Many2one('hr.department', 'Business Unit', readonly=True, required=True)
    target = fields.Float('Revenue Target', readonly=False)
    revenue_achieved = fields.Float(' Revenue Achievement', readonly=True)
    percentage = fields.Float('Percentage %', compute=_compute_percentage, store=True, readonly=True)
    leads_achieved = fields.One2many('bu.leads.achieved', 'ref_id', 'BU Achievement Breakup', readonly=True)

    @api.model
    def bu_target(self):
        bu_target = {}
        crm_total_ids = []
        current_date = datetime.date.today().month
        month = datetime.date.today().month
        year = datetime.date.today().year
        l1 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
        l2 = [1, 2, 3]
        if month in l1:
            start_date = str(year) + '_' + '04_01'
            end_date = str(int(year) + 1) + '_' + '03_31'
        else:
            start_date = str(int(year) - 1) + '_' + '04_01'
            end_date = str(year) + '_' + '03_31'
        selfObj = self.env['bu.achievement']
        crmLeadObj = self.env['crm.lead']
        leads_achievedObj = self.env['bu.leads.achieved']
        stage_id = ''
        stage_ids = self.env['crm.case.stage'].search([('probability', '=', 100.0)])[0]
        if stage_ids:
            stage_id = stage_ids.id
        bu_ids = self.env['hr.department'].search([('dept_main_category', '=', 'Non Support')])
        for bu in bu_ids:
            domain = [('department_id', '=', bu.id), ('closed_won_date', '>=', start_date),
                      ('closed_won_date', '<=', end_date), ('stage_id', '=', stage_id)]
            if bu.dept_category == "Service" or "Temenos":
                if bu.parent_id.dept_code:
                    bu_id = bu.parent_id.id
                elif bu.parent_id.parent_id.dept_code:
                    bu_id = bu.parent_id.parent_id.id
                else:
                    bu_id = bu.id
            else:
                if bu.parent_id:
                    bu_id = bu.parent_id.id
                elif bu.parent_id.parent_id:
                    bu_id = bu.parent_id.parent_id.id
                else:
                    bu_id = bu.id
            if bu_id not in bu_target:
                bu_target[bu_id] = 0.0
            bu_achievement_ids = selfObj.search([('department_id', '=', bu_id)])
            if not bu_achievement_ids:
                bu_achievement_ids = selfObj.create({'department_id': bu_id})
            crm_ids = crmLeadObj.search(domain)
            for record in crm_ids:
                crm_total_ids.append(record.id)
                bu_target[bu_id] += record.planned_revenue
                bu_leads_achieved = leads_achievedObj.search([('lead_id', '=', record.id),
                                                              ('ref_id', '=', bu_achievement_ids.id)])
                if not bu_leads_achieved:
                    bu_leads_achieved.create({'lead_id': record.id,
                                              'ref_id': bu_achievement_ids.id,
                                              })
            bu_achievement_ids.revenue_achieved = bu_target[bu_id]

        # Unlink process for previous closures #

        leads_achieved_ids = [leads_achieved.id for leads_achieved in leads_achievedObj.search([
            ('lead_id', 'in', crm_total_ids)])]

        total_leads_achieved_ids = [leads_achieved.id for leads_achieved in leads_achievedObj.search([
            ('id', '!=', False)])]

        unlink_ids = list(set(total_leads_achieved_ids) - set(leads_achieved_ids))

        for unlink_id in unlink_ids:
            self.pool.get('bu.leads.achieved').unlink(self._cr, self._uid, unlink_id, self._context)

