# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line","order.line.position.mixin"]
