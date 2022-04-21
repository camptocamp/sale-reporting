# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_group_currency_id = fields.Many2one(
        "res.currency",
        string="Group Currency",
        config_parameter="base_group_currency.group_currency_id",
    )
