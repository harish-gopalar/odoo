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


class incentive_result_line(models.Model):
    _name = 'incentive.result.line'
    _description = 'Incentive Result Line'

    name = fields.Char('Incentive for the Product', readonly=True)
    amount = fields.Float('Amount(US$)', readonly=True)
    ref_id = fields.Many2one('incentive.simulation', 'Reference', readonly=True)


class incentive_product_line(models.Model):
    _name = 'incentive.product.line'
    _description = 'Incentive Product Line'

    name = fields.Char('Product', readonly=True)
    markup = fields.Float('Markup %')
    ref_id = fields.Many2one('incentive.simulation', 'Reference', readonly=True)


class product_line(models.Model):
    _name = 'product.line'
    _description = 'Product Line'

    name = fields.Char('Product', readonly=True)
    amount = fields.Float('Amount', default=0.0)
    ref_id = fields.Many2one('incentive.simulation', 'Reference', readonly=True)


class incentive_simulation(models.Model):
    _name = 'incentive.simulation'
    _inherit = ['mail.thread']
    _description = 'Incentive Simulation'
    _order = "id desc"
    _rec_name = "designation"

    @api.one
    @api.depends('target', 'achievement', )
    def _compute_percentage(self):
        for record in self:
            if record.target:
                record.achievement_percentage = record.achievement * 100.0 / record.target
            else:
                record.achievement_percentage = 0.0

    @api.one
    @api.depends('product_line_ids.amount')
    def _compute_achievement(self):
        total_achievement = 0.0
        for record in self:
            for product_id in record.product_line_ids:
                total_achievement += product_id.amount
            record.achievement = float(total_achievement)

    @api.one
    @api.depends('target', 'achievement', 'designation', 'incentive_product_line_ids', 'incentive_result_line_ids', 'product_line_ids', 'achievement_percentage')
    def _compute_incentive_total(self):
        jmr_software_sale = 0.0
        third_party_software = 0.0
        professional_services = 0.0
        implementation_delivery = 0.0
        hardware_technology = 0.0
        total_incentive = 0.0
        for record in self:
            collection_days_percentage = 0.0
            collection_days = [collection_days_id.markup for collection_days_id in record.incentive_product_line_ids
                               if collection_days_id.name == 'Collection days']

            if collection_days:
                if collection_days[0] <= 60:
                    collection_days_percentage = 100.0
                elif 89 >= collection_days[0] > 60:
                    collection_days_percentage = 75.0
                elif 120 >= collection_days[0] >= 90:
                    collection_days_percentage = 50.0
                elif 150 >= collection_days[0] > 120:
                    collection_days_percentage = 25.0
                else:
                    collection_days_percentage = 0.0
            for product_id in record.product_line_ids:
                if product_id.name == 'JMRi Software/License sale':
                    if record.achievement_percentage >= 100:
                        if record.designation == 'Sales Manager':
                            incentive = 4
                        else:
                            incentive = 2
                    else:
                        if record.designation == 'Sales Manager':
                            incentive = 3
                        else:
                            incentive = 1.5
                    jmr_software_sale = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                         * float(incentive)) / 100
                elif product_id.name == 'Third Party Software/ License Sale':
                    percentage = 0.0
                    markup = [third_party_software_id.markup for third_party_software_id in record.incentive_product_line_ids
                              if third_party_software_id.name == 'Third Party Software/ License Sale']
                    if record.achievement_percentage >= 100:
                        if markup:
                            if markup[0] >= 100:
                                if record.designation == 'Sales Manager':
                                    percentage = 4
                                else:
                                    percentage = 2
                            elif 100 > markup[0] >= 75:
                                if record.designation == 'Sales Manager':
                                    percentage = 3
                                else:
                                    percentage = 1.5
                            elif 75 > markup[0] >= 50:
                                if record.designation == 'Sales Manager':
                                    percentage = 1.5
                                else:
                                    percentage = 1
                            elif 50 > markup[0] >= 25:
                                if record.designation == 'Sales Manager':
                                    percentage = 1
                                else:
                                    percentage = 0.6
                            elif 25 > markup[0] >= 15:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.5
                                else:
                                    percentage = 0.4
                            else:
                                percentage = 0
                        third_party_software = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                                * float(percentage)) / 100
                    else:
                        if markup:
                            if markup[0] >= 100:
                                if record.designation == 'Sales Manager':
                                    percentage = 3
                                else:
                                    percentage = 1.5
                            elif 100 > markup[0] >= 75:
                                if record.designation == 'Sales Manager':
                                    percentage = 2.25
                                else:
                                    percentage = 1.10
                            elif 75 > markup[0] >= 50:
                                if record.designation == 'Sales Manager':
                                    percentage = 1.25
                                else:
                                    percentage = 0.75
                            elif 50 > markup[0] >= 25:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.75
                                else:
                                    percentage = 0.5
                            elif 25 > markup[0] >= 15:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.4
                                else:
                                    percentage = 0.25
                            else:
                                percentage = 0
                        third_party_software = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                                * float(percentage)) / 100

                elif product_id.name == 'Professional Services':
                    if record.achievement_percentage >= 100:
                        if record.designation == 'Sales Manager':
                            incentive = 2
                        else:
                            incentive = 0.5
                    else:
                        if record.designation == 'Sales Manager':
                            incentive = 1.5
                        else:
                            incentive = 0.45
                    professional_services = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                             * float(incentive)) / 100

                elif product_id.name == 'Implementation & Delivery':
                    if record.achievement_percentage >= 100:
                        if record.designation == 'Sales Manager':
                            incentive = 2
                        else:
                            incentive = 0.5
                    else:
                        if record.designation == 'Sales Manager':
                            incentive = 1.5
                        else:
                            incentive = 0.45
                    implementation_delivery = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                               * float(incentive)) / 100

                elif product_id.name == 'Hardware & Technology':
                    percentage = 0.0
                    markup = [third_party_software_id.markup for third_party_software_id in record.incentive_product_line_ids
                              if third_party_software_id.name == 'Hardware & Technology']
                    if record.achievement_percentage >= 100:
                        if markup:
                            if markup[0] >= 100:
                                if record.designation == 'Sales Manager':
                                    percentage = 4
                                else:
                                    percentage = 2
                            elif 100 > markup[0] >= 75:
                                if record.designation == 'Sales Manager':
                                    percentage = 3
                                else:
                                    percentage = 1.5
                            elif 75 > markup[0] >= 50:
                                if record.designation == 'Sales Manager':
                                    percentage = 1.5
                                else:
                                    percentage = 1
                            elif 50 > markup[0] >= 25:
                                if record.designation == 'Sales Manager':
                                    percentage = 1
                                else:
                                    percentage = 0.6
                            elif 25 > markup[0] >= 15:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.5
                                else:
                                    percentage = 0.4
                            else:
                                percentage = 0
                        hardware_technology = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                               * float(percentage)) / 100
                    else:
                        if markup:
                            if markup[0] >= 100:
                                if record.designation == 'Sales Manager':
                                    percentage = 3
                                else:
                                    percentage = 1.5
                            elif 100 > markup[0] >= 75:
                                if record.designation == 'Sales Manager':
                                    percentage = 2.25
                                else:
                                    percentage = 1.10
                            elif 75 > markup[0] >= 50:
                                if record.designation == 'Sales Manager':
                                    percentage = 1.25
                                else:
                                    percentage = 0.75
                            elif 50 > markup[0] >= 25:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.75
                                else:
                                    percentage = 0.5
                            elif 25 > markup[0] >= 15:
                                if record.designation == 'Sales Manager':
                                    percentage = 0.4
                                else:
                                    percentage = 0.25
                            else:
                                percentage = 0
                        hardware_technology = ((float(product_id.amount) * float(collection_days_percentage)) / 100
                                               * float(percentage)) / 100
            for incentive_id in record.incentive_result_line_ids:
                if incentive_id.name == 'JMRi Software/License sale':
                    incentive_id.amount = jmr_software_sale
                elif incentive_id.name == 'Third Party Software/ License Sale':
                    incentive_id.amount = third_party_software
                elif incentive_id.name == 'Professional Services':
                    incentive_id.amount = professional_services

                elif incentive_id.name == 'Implementation & Delivery':
                    incentive_id.amount = implementation_delivery
                elif incentive_id.name == 'Hardware & Technology':
                    incentive_id.amount = hardware_technology
                else:
                    pass
            for product_id in record.incentive_result_line_ids:
                total_incentive += product_id.amount
            record.total_incentive = float(total_incentive)

    sales_person_id = fields.Many2one('saleperson.target', 'Sales Person', readonly=True, required=True)
    designation = fields.Selection([('Sales Manager', 'Sales Manager'), ('Regional Director', 'Regional Director')],
                                   'Designation: ', readonly=True, invisible=1)
    target = fields.Float('Target', required=True, default=0.0)
    achievement = fields.Float('Achievement', readonly=True, default=0.0, compute=_compute_achievement, store=True)
    total_incentive = fields.Float('Total Incentive', readonly=True, default=0.0,
                                   compute=_compute_incentive_total, store=True)
    achievement_percentage = fields.Float('Achievement % YTD', required=True, readonly=True, default=0.0,
                                          compute=_compute_percentage, store=True)
    product_line_ids = fields.One2many('product.line', 'ref_id', 'Product Line IDs')
    incentive_product_line_ids = fields.One2many('incentive.product.line', 'ref_id', 'Incentive Product Line IDs')
    incentive_result_line_ids = fields.One2many('incentive.result.line', 'ref_id', 'Incentive Result Line IDs')
    calculation_info = fields.Text('Calculation Info', readonly=True)
    label = fields.Boolean('* Green and Blue Color fields are editable', readonly=True)
    sales_manager = fields.Many2one('res.users', 'Sales Manager', readonly=True)

    _sql_constraints = {('designation_uniq', 'unique(sales_person_id)',
                         ' For this Sales Person Incentive simulation already created.')}

    @api.model
    def create(self, vals):
        info = '1) Receipt of all payments from clients –  Quarterly incentive will be calculated on the payments received \n' \
               '2) On Services Engagement only Professional Fees  will be considered as revenue for incentive calculation \n' \
               '3) For Product Sales – License Cost  and implementation fees (professional fees) will be considered  for  Revenue \n' \
               '4) For fixed  cost  projects, the cost of the project should not exceed  the budgeted cost \n' \
               '5) For long term post implementation engagement, you will get the incentive for maximum  12 months from the same client. \n' \
               '6) Payout  - Quarterly - Apr- Jun (Payout Max by July End), July -Sep (Max By October End), Oct - Dec (Max by Jan), Jan to Mar (Max By April End) \n' \
               '7)  Leads in the territory will by default go the assigned sales manager. \n ' \
               '8) Payments should be received within the maximum of  2 months of payment due date. 75 percent incentive will be paid on more than 60 but less than ' \
               '90 days  90 to 120 days  - Only 50% of the incentive amount. More than 120 days  < 150 Days only 25% incentive. No incentive above 150 days ' \
               '( This will be applicable only if the delay in payment is not because of any fault of JMRi) \n' \
               '9) Any written off invoiced amount due to no fault of the organization will be recovered from future incentives of the sales staff  (This will be decided on case to case basis) \n' \
               '10) No deal should be done without an underlying contract \n' \
               '11) Apart from the sales incentive sales staff may also be eligible for any discretionary bonuses based on companys performance and over achievement of targets. \n' \
               '12) Employee should be on our payroll and not serving notice period \n' \
               '13) Where there are no sales managers  - Regional Manager will be entitled to get the sales Manager Incentives \n' \
               '14) If the Sales Manager is on Leave and the lead is handled by another sales manager then the incentive will be shared by both in 50:50 proportion \n'

        vals['calculation_info'] = info
        incentive_id = super(incentive_simulation, self).create(vals)

        product_lines = ['JMRi Software/License sale', 'Third Party Software/ License Sale', 'Professional Services',
                         'Implementation & Delivery', 'Hardware & Technology']
        for product in product_lines:
            self.env['product.line'].create({'name': product,
                                             'ref_id': incentive_id.id,
                                             })

        product_lines = ['Third Party Software/ License Sale', 'Hardware & Technology', 'Collection days']
        for product in product_lines:
            self.env['incentive.product.line'].create({'name': product,
                                                       'ref_id': incentive_id.id,
                                                       })

        product_lines = ['JMRi Software/License sale', 'Third Party Software/ License Sale', 'Professional Services',
                         'Implementation & Delivery', 'Hardware & Technology']
        for product in product_lines:
            self.env['incentive.result.line'].create({'name': product,
                                                      'ref_id': incentive_id.id,
                                                      })
        saleperson_target_ids = incentive_id.sales_person_id.manager_user_relation_id.saleperson_target_line
        if len(saleperson_target_ids) > 1:
            if incentive_id.sales_person_id.manager_user_relation_id.user_id.id == incentive_id.sales_person_id.user_id.id:
                incentive_id.designation = 'Regional Director'
            else:
                incentive_id.designation = 'Sales Manager'
        else:
            incentive_id.designation = 'Sales Manager'

        return incentive_id

    @api.model
    def incentive_creation_schedule(self):
        selfObj = self.env['incentive.simulation']
        saleperson_target_ids = self.env['saleperson.target'].search([('manager_user_relation_id', '!=', False)])
        for fields_user in saleperson_target_ids:
            sales_target = selfObj.search([('sales_person_id', '=', fields_user.id)])
            if not sales_target:
                sales_target = selfObj.create({'sales_person_id': fields_user.id})
                if sales_target.sales_person_id.manager_user_relation_id.user_id:
                    sales_target.sales_manager = sales_target.sales_person_id.manager_user_relation_id.user_id.id
