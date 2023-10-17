# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.calc_order_lines_dependencies()
        return records

    def write(self, vals):
        result = super().write(vals)
        if "order_line" in vals:
            self.calc_order_lines_dependencies()
        return result

    def calc_order_lines_dependencies(self):
        """Link order lines with their respective siblings"""
        self.order_line.write({"previous_line_id": False, "next_line_id": False})
        for order in self:
            previous_line = False
            for order_line in order.order_line.sorted("sequence"):
                order_line.previous_line_id = previous_line
                if previous_line:
                    previous_line.next_line_id = order_line
                previous_line = order_line
