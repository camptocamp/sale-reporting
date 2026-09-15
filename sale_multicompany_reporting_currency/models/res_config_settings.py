# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multicompany_reporting_amount = fields.Selection(
        [
            ("total", "Amount total"),
            ("untaxed", "Untaxed Amount"),
        ],
        config_parameter="sale_multicompany_reporting_currency.multicompany_reporting_amount",
        default="total",
    )
