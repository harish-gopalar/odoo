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
from datetime import timedelta


class manual_schedule_actions(models.Model):
    _name = 'manual.schedule.actions'
    _inherit = ['mail.thread']
    _description = 'Manual Schedule Action'

    name = fields.Char('Name')

    @api.multi
    def run_annual_performance(self):
        return self.env['annual.performance.sheet'].sudo().annual_performance_sheet_schedule()

    @api.multi
    def run_active_pipe(self):
        return self.env['crm.lead'].sudo().checking_opportunity_active_pipe()

    @api.multi
    def run_opportunity_pipeline_build(self):
        return self.env['opportunity.pipeline.build'].sudo().run_opportunity_pipeline_build()

    @api.multi
    def run_bu_pipeline_build(self):
        return self.env['bu.pipeline.build'].sudo().run_bu_opportunity_pipeline_build()

    @api.multi
    def run_omm_mismatch(self):
        return self.env['crm.omm'].sudo().check_mismatch_omm()

    @api.multi
    def run_omm_expiry_mail(self):
        return self.env['crm.sales.target'].sudo().omm_expiry_mail_trigger()

    @api.multi
    def run_account_mapping(self):
        return self.env['account.mapping'].sudo().run_account_mapping_schedule()

    @api.multi
    def run_levels_of_account_schedule(self):
        field_seller_ids = self.env['res.users'].search([('sales_category', '=', 'FieldSales')])
        for field_user in field_seller_ids:
            self.env['crm.user.account.target.line'].sudo().update_level(seller_id=field_user)
        return True

    @api.multi
    def run_bu_account_mapping(self):
        return self.env['bu.account.mapping'].sudo().run_bu_account_mapping()

    @api.multi
    def run_seller_account_mapping(self):
        return self.env['seller.account.mapping'].sudo().run_seller_account_mapping(seller_id=None)

    @api.multi
    def run_bu_active_pipe(self):
        return self.env['bu.active.pipe'].sudo().run_bu_active_pipe()

    @api.multi
    def run_seller_active_pipe(self):
        return self.env['seller.active.pipe'].sudo().run_seller_active_pipe()

    @api.multi
    def run_bu_committed_closures(self):
        return self.env['bu.committed.closures'].sudo().bu_committed_closures()

    @api.multi
    def run_ob_revenue_update(self):
        return self.env['bu.order.booking'].sudo().bu_ob_targets()

    @api.multi
    def run_seller_ob_revenue_update(self):
        return self.env['seller.order.booking'].sudo().sellers_ob_targets()

    @api.multi
    def run_update_principal_meeting_details(self):
        return self.env['principal.contact'].sudo().update_principal_meeting_details()

    @api.multi
    def update_variant_values(self):
        for record in self.env['bu.achievement'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['bu.quarter.wise'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['bu.order.booking'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['seller.order.booking'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['seller.quarter.wise'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['seller.bu.quarter.wise'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['bu.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['bu.quarter.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['seller.bu.opportunity.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['seller.opportunity.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['opportunity.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['bu.quarter.pipeline.build'].search([]):
            record.sudo()._pipeline_build_achievement()
        for record in self.env['seller.planned.active.line'].search([]):
            record.sudo()._compute_percentage()
        for record in self.env['bu.planned.active.line'].search([]):
            record.sudo()._compute_percentage()
        return True

    @api.multi
    def run_sales_commission(self):
        return self.env['sales.commission.configuration'].sudo().compute_commission()




