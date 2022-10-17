# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class BlanketOrder(models.Model):
    _name = "sale.blanket.order"
    _inherit = ["sale.blanket.order", "order.position.mixin"]
