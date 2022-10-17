# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class OrderPositionMixin(models.AbstractModel):
    _name = "order.position.mixin"
    _description = "Order position mixin"

    locked_positions = fields.Boolean(compute="_compute_locked_positions")

    @api.depends("state")
    def _compute_locked_positions(self):
        for record in self:
            record.locked_positions = record.state != "draft"

    def action_confirm(self):
        self.recompute_positions()
        return super().action_confirm()

    def action_quotation_send(self):
        self.recompute_positions()
        return super().action_quotation_send()

    def recompute_positions(self):
        for sale in self:
            if sale.locked_positions or sale.company_id.disable_sale_position_recompute:
                continue
            lines = sale.order_line.filtered(lambda l: not l.display_type)
            lines.sorted(key=lambda x: (x.sequence, x.id))
            for position, line in enumerate(lines, start=1):
                line.position = position


class OrderLinePositionMixin(models.AbstractModel):
    _name = "order.line.position.mixin"
    _description = "Order line position mixin"

    position = fields.Integer(readonly=True, index=True, default=False)
    position_formatted = fields.Char(compute="_compute_position_formatted")

    @api.depends("position")
    def _compute_position_formatted(self):
        for record in self:
            record.position_formatted = record._format_position(record.position)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = self._add_next_position_on_new_line(vals_list)
        return super().create(vals_list)

    def unlink(self):
        sales = self.mapped("order_id")
        res = super().unlink()
        for sale in sales:
            sale.recompute_positions()
        return res

    def _add_next_position_on_new_line(self, vals_list):
        # TODO: Check this if we can easily adapt it to both SOL and Blanket line
        # the queries needs to be adapted and there is no POS in blanket
        sale_ids = [
            line["order_id"]
            for line in vals_list
            if not line.get("display_type") and line.get("order_id")
        ]
        if sale_ids:
            ids = tuple(set(sale_ids))
            self.flush()
            query = """
            SELECT order_id, max(position) FROM sale_order_line
            WHERE order_id in %s GROUP BY order_id;
            """
            self.env.cr.execute(query, (ids,))
            default_pos = {key: 1 for key in ids}
            existing_pos = {
                order_id: pos + 1 for order_id, pos in self.env.cr.fetchall()
            }
            sale_pos = {**default_pos, **existing_pos}
            for line in vals_list:
                if not line.get("display_type"):
                    line["position"] = sale_pos[line["order_id"]]
                    sale_pos[line["order_id"]] += 1
        return vals_list

    @api.model
    def _format_position(self, position):
        if not position:
            return ""
        return str(position).zfill(3)
