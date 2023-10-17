# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create(self, vals_list):
        records = super().create(vals_list)
        records.compute_order_lines_dependency()
        return records

    def write(self, vals):
        result = super().write(vals)
        self.compute_order_lines_dependency()
        return result

    @api.depends("order_line")
    def compute_order_lines_dependency(self):
        """Link order lines with their respective siblings"""
        for order in self:
            previous_line = False
            for order_line in order.order_line.sorted("sequence"):
                order_line.previous_line_id = previous_line
                if previous_line:
                    previous_line.next_line_id = order_line
                previous_line = order_line
