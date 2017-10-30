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
import xlwt
import cStringIO
import base64
import datetime


def font_style(position='left', bold=0, fontos=0, font_height=200, border=0, color=False):
    font = xlwt.Font()
    font.name = 'Verdana'
    font.bold = bold
    font.height = font_height
    center = xlwt.Alignment()
    center.horz = xlwt.Alignment.HORZ_CENTER
    center.vert = xlwt.Alignment.VERT_CENTER
    center.wrap = xlwt.Alignment.VERT_JUSTIFIED

    left = xlwt.Alignment()
    left.horz = xlwt.Alignment.HORZ_LEFT
    left.vert = xlwt.Alignment.VERT_CENTER
    left.wrap = xlwt.Alignment.VERT_JUSTIFIED

    right = xlwt.Alignment()
    right.horz = xlwt.Alignment.HORZ_RIGHT
    right.vert = xlwt.Alignment.VERT_CENTER
    right.wrap = xlwt.Alignment.VERT_JUSTIFIED

    borders = xlwt.Borders()
    borders.right = 1
    borders.left = 1
    borders.top = 1
    borders.bottom = 1

    orient = xlwt.Alignment()
    orient.orie = xlwt.Alignment.ORIENTATION_90_CC

    style = xlwt.XFStyle()

    if border == 1:
        style.borders = borders

    if fontos == 'red':
        font.colour_index = 2
        style.font = font
    else:
        style.font = font

    if position == 'center':
        style.alignment = center
    elif position == 'right':
        style.alignment = right
    else:
        style.alignment = left
    if color == 'grey':
        badBG = xlwt.Pattern()
        badBG.pattern = badBG.SOLID_PATTERN
        badBG.pattern_fore_colour = 22
        style.pattern = badBG
    if color == 'red':
        badBG = xlwt.Pattern()
        badBG.pattern = badBG.SOLID_PATTERN
        badBG.pattern_fore_colour = 5
        style.pattern = badBG

    if color == 'yellow':
        badBG = xlwt.Pattern()
        badBG.pattern = badBG.SOLID_PATTERN
        badBG.pattern_fore_colour = 0x0D
        style.pattern = badBG

    return style


class account_summary_report(models.TransientModel):
    _name = 'account.summary.report'
    _description = 'Account Summary Report'
    _order = "id desc"

    user_id = fields.Many2one('res.users', 'Field SalesPerson')
    country_id = fields.Many2one('res.country', 'Country')
    department_id = fields.Many2one('hr.department', 'Business Unit')
    file_name = fields.Binary('Report')
    name = fields.Char('Name')
    account_status = fields.Selection([('Active', 'Active'), ('Inactive', 'Inactive')], 'Account Status')
    attachment_id = fields.Many2one('ir.attachment', string="Attachments")

    @api.multi
    def account_summary_report(self):
        filename = 'Account Summary Report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        style = xlwt.XFStyle()
        style.alignment.wrap = 1
        worksheet = wb.add_sheet("Account Summary Report")
        M_header_tstyle = font_style(position='center', bold=1, border=1, fontos='black', font_height=700, color='grey')
        header_tstyle_c = font_style(position='center', bold=1, border=1, fontos='black', font_height=180, color='grey')

        colList = ["Account ID", "Account Name", "Account Creation date", "Account Status", "Country", "Contacts Name",
                   "Designation", "Contacts Count", "Lead ID", "Lead Name", "Leads Count", "Opportunity ID",
                   "Opportunity Name", "Opportunity Count", "Last Meeting Date", "Last Meeting Subject",
                   "Last Meeting Organized By", "Meeting Count", "Last Called Date", "Calls Count", "Last Email Date",
                   "Emails Count", "Levels Of Account", "Industry Category", "Sub Industry", "Inside Sales",
                   "Sales Person", "Alt Email", "Email", "Fax", "Mobile", "Alt Phone", "Phone", "Website"]
        worksheet.row(0).height = 256 * 3
        worksheet.write_merge(0, 0, 0, 33, 'Account Summary Report', M_header_tstyle)
        worksheet.write_merge(1, 1, 0, 3, 'Account', header_tstyle_c)
        worksheet.write(1, 4, '', header_tstyle_c)
        worksheet.write_merge(1, 1, 5, 7, 'Contacts', header_tstyle_c)
        worksheet.write_merge(1, 1, 8, 10, 'Leads', header_tstyle_c)
        worksheet.write_merge(1, 1, 11, 13, 'Opportunity', header_tstyle_c)
        worksheet.write_merge(1, 1, 14, 17, 'Meetings', header_tstyle_c)
        worksheet.write_merge(1, 1, 18, 19, 'PhoneCalls', header_tstyle_c)
        worksheet.write_merge(1, 1, 20, 21, 'Emails', header_tstyle_c)
        worksheet.write_merge(1, 1, 22, 33, '', header_tstyle_c)
        j = 2
        worksheet.row(2).height = 256 * 2
        worksheet.row(1).height = 256 * 2
        for c in range(len(colList)):
            worksheet.col(c).width = 256 * 20
            worksheet.write(j, c, colList[c], header_tstyle_c)
        j += 1
        res_partnerObj = self.env['res.partner']
        crm_leadObj = self.env['crm.lead']
        meetingObj = self.env['calendar.event']
        phonecallObj = self.env['crm.phonecall']
        emailObj = self.env['crm.email.log']
        domain = [('customer', '=', True), ('is_company', '=', True), ]
        if self.user_id:
            domain += [('user_id', '=', self.user_id.id), ]
        if self.account_status:
            domain += [('account_status', '=', self.account_status), ]
        account_ids = res_partnerObj.search(domain)
        for account_id in account_ids:
            lead_name = ''
            lead_ref = ''
            opportunity_name = ''
            opportunity_ref = ''
            last_meeting_date = ''
            last_meeting_subject = ''
            last_meeting_organized = ''
            last_phonecall_date = ''
            last_email_date = ''
            i = -1
            worksheet.write(j, i + 1, account_id.id or '')
            worksheet.write(j, i + 2, account_id.name or '')
            worksheet.write(j, i + 3, account_id.create_date or '')
            worksheet.write(j, i + 4, account_id.account_status or '')
            worksheet.write(j, i + 5, account_id.country_id.name or '')
            worksheet.write(j, i + 8, account_id.contact_count)
            account_lead_ids = crm_leadObj.search([('partner_id', '=', account_id.id)])
            for lead_id in account_lead_ids:
                if lead_id.type == 'lead':
                    lead_name += str(lead_id.name) + ', '
                    if lead_id.lead_ref_no:
                        lead_ref += str(lead_id.lead_ref_no) + ', '
                else:
                    opportunity_name += str(lead_id.name) + ', '
                    if lead_id.opp_ref_no:
                        opportunity_ref += str(lead_id.opp_ref_no) + ', '
            worksheet.write(j, i + 9, lead_name)
            worksheet.write(j, i + 10, lead_ref)
            worksheet.write(j, i + 11, account_id.lead_count)
            worksheet.write(j, i + 12, opportunity_name)
            worksheet.write(j, i + 13, opportunity_ref)
            worksheet.write(j, i + 14, account_id.opportunity_count)
            account_meeting_ids = meetingObj.search([('account_id', '=', account_id.id)])
            if account_meeting_ids:
                last_meeting_date = account_meeting_ids[0].meeting_date
                last_meeting_subject = account_meeting_ids[0].name
                last_meeting_organized = account_meeting_ids[0].meeting_user_id.name

            worksheet.write(j, i + 15, last_meeting_date)
            worksheet.write(j, i + 16, last_meeting_subject)
            worksheet.write(j, i + 17, last_meeting_organized)
            worksheet.write(j, i + 18, account_id.meeting_count)

            account_phonecall_ids = phonecallObj.search([('parent_id', '=', account_id.id)])
            if account_phonecall_ids:
                last_phonecall_date = account_phonecall_ids[0].date
            worksheet.write(j, i + 19, last_phonecall_date)
            worksheet.write(j, i + 20, account_id.phonecall_count)
            account_email_ids = emailObj.search([('parent_id', '=', account_id.id)])
            if account_email_ids:
                last_email_date = account_email_ids[0].date
            worksheet.write(j, i + 21, last_email_date)
            worksheet.write(j, i + 22, account_id.email_count)
            worksheet.write(j, i + 23, account_id.levels_of_account or '')
            worksheet.write(j, i + 24, account_id.industry_category_id.name or '')
            worksheet.write(j, i + 25, account_id.industry_id.name or '')
            worksheet.write(j, i + 26, account_id.inside_user_id.name or '')
            worksheet.write(j, i + 27, account_id.user_id.name or '')
            worksheet.write(j, i + 28, account_id.alt_email or '')
            worksheet.write(j, i + 29, account_id.email or '')
            worksheet.write(j, i + 30, account_id.fax or '')
            worksheet.write(j, i + 31, account_id.mobile or '')
            worksheet.write(j, i + 32, account_id.alt_phone or '')
            worksheet.write(j, i + 33, account_id.phone or '')
            worksheet.write(j, i + 34, account_id.website or '')
            if account_id.child_ids:
                for child_id in account_id.child_ids:
                    child_lead_name = ''
                    child_lead_ref = ''
                    child_opportunity_name = ''
                    child_opportunity_ref = ''
                    child_last_meeting_date = ''
                    child_last_meeting_subject = ''
                    child_last_meeting_organized = ''
                    child_last_phonecall_date = ''
                    child_last_email_date = ''
                    j += 1
                    worksheet.write(j, i + 6, child_id.name or '')
                    worksheet.write(j, i + 7, child_id.function or '')
                    # worksheet.write(j, i + 8, child_id.contact_count)
                    child_lead_ids = crm_leadObj.search([('partner_contact_id', '=', child_id.id)])
                    for lead_id in child_lead_ids:
                        if lead_id.type == 'lead':
                            child_lead_name += str(lead_id.name) + ', '
                            if lead_id.lead_ref_no:
                                child_lead_ref += str(lead_id.lead_ref_no) + ', '
                        else:
                            child_opportunity_name += str(lead_id.name) + ', '
                            if lead_id.opp_ref_no:
                                child_opportunity_ref += str(lead_id.opp_ref_no) + ', '

                    worksheet.write(j, i + 9, child_lead_ref)
                    worksheet.write(j, i + 10, child_lead_name)
                    worksheet.write(j, i + 11, child_id.lead_count)

                    worksheet.write(j, i + 13, child_opportunity_name)
                    worksheet.write(j, i + 12, child_opportunity_ref)
                    worksheet.write(j, i + 14, child_id.opportunity_count)

                    child_meeting_ids = meetingObj.search([('meeting_contact_id', '=', child_id.id)])
                    if child_meeting_ids:
                        child_last_meeting_date = child_meeting_ids[0].meeting_date
                        child_last_meeting_subject = child_meeting_ids[0].name
                        child_last_meeting_organized = child_meeting_ids[0].meeting_user_id.name

                    worksheet.write(j, i + 15, child_last_meeting_date)
                    worksheet.write(j, i + 16, child_last_meeting_subject)
                    worksheet.write(j, i + 17, child_last_meeting_organized)
                    worksheet.write(j, i + 18, child_id.meeting_count)

                    child_phonecall_ids = phonecallObj.search([('partner_id', '=', child_id.id)])
                    if child_phonecall_ids:
                        child_last_phonecall_date = child_phonecall_ids[0].date
                    worksheet.write(j, i + 19, child_last_phonecall_date)
                    worksheet.write(j, i + 20, child_id.phonecall_count)
                    child_email_ids = emailObj.search([('partner_id', '=', child_id.id)])
                    if child_email_ids:
                        child_last_email_date = child_email_ids[0].date
                    worksheet.write(j, i + 21, child_last_email_date)
                    worksheet.write(j, i + 22, child_id.email_count)
                    worksheet.write(j, i + 23, child_id.levels_of_account or '')
                    worksheet.write(j, i + 24, child_id.industry_category_id.name or '')
                    worksheet.write(j, i + 25, child_id.industry_id.name or '')
                    worksheet.write(j, i + 26, child_id.inside_user_id.name or '')
                    worksheet.write(j, i + 27, child_id.user_id.name or '')
                    worksheet.write(j, i + 28, child_id.alt_email or '')
                    worksheet.write(j, i + 29, child_id.email or '')
                    worksheet.write(j, i + 30, child_id.fax or '')
                    worksheet.write(j, i + 31, child_id.mobile or '')
                    worksheet.write(j, i + 32, child_id.alt_phone or '')
                    worksheet.write(j, i + 33, child_id.phone or '')
                    worksheet.write(j, i + 34, child_id.website or '')
            j += 1
        fp = cStringIO.StringIO()
        wb.save(fp)
        out = base64.encodestring(fp.getvalue())
        self.write({'file_name': out, 'name': filename})
        return {
            'domain': [('id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.summary.report',
            'target': 'current',
            'nodestroy': True,
            'type': 'ir.actions.act_window',
            'name': 'Account Summary Report',
            'res_id': self.id,
        }

