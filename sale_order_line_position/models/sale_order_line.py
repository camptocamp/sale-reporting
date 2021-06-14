# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    position = fields.Integer(readonly=True, index=True, default=False)
    position_formatted = fields.Char(compute="_compute_position_formatted")

    @api.depends("position")
    def _compute_position_formatted(self):
        for record in self:
            record.position_formatted = record._format_position(record.position)

    @api.onchange("sequence")
    def _onchange_sequence(self):
        if self.order_id.locked_positions:
            return
        lines = self.order_id.order_line.filtered(
            lambda x: not x.display_type and x.sequence < self.sequence
        )
        self.position = len(lines) + 1

    @api.model_create_multi
    def create(self, vals_list):
        sale_ids = [
            line["order_id"]
            for line in vals_list
            if not line.get("display_type") and line.get("order_id")
        ]
        sale_pos = {}
        sales = self.env["sale.order"].browse(sale_ids)
        for sale in sales:
            sale_pos[sale.id] = sale._get_next_position_number()
        for line in vals_list:
            if not line.get("display_type"):
                line["position"] = sale_pos[line["order_id"]]
                sale_pos[line["order_id"]] += 1
        return super().create(vals_list)

    def unlink(self):
        sales = self.mapped("order_id")
        res = super().unlink()
        for sale in sales:
            sale.recompute_position()
        return res

    @api.model
    def _format_position(self, position):
        if not position:
            return ""
        return str(position).zfill(3)
