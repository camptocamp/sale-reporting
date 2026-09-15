# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.model
    def _get_multicompany_reporting_amount_key(self):
        return "sale_multicompany_reporting_currency.multicompany_reporting_amount"

    @api.model_create_multi
    def create(self, vals_list):
        params = super().create(vals_list)
        if params._multicompany_reporting_amount_needs_update():
            self._update_multicompany_reporting_amount()
        return params

    def write(self, vals):
        res = super().write(vals)
        needs_update = self._multicompany_reporting_amount_needs_update()
        if {"key", "value"}.intersection(vals) and needs_update:
            self._update_multicompany_reporting_amount()
        return res

    def unlink(self):
        needs_update = self._multicompany_reporting_amount_needs_update()
        res = super().unlink()
        if needs_update:
            self._update_multicompany_reporting_amount()
        return res

    def _multicompany_reporting_amount_needs_update(self):
        return self._get_multicompany_reporting_amount_key() in self.mapped("key")

    @api.model
    def _update_multicompany_reporting_amount(self):
        # The reporting amount option (total/untaxed) isn't part of the
        # `multicompany.reporting.currency.mixin` API, so there is no field to
        # write to trigger the recompute of `amount_multicompany_reporting_currency`.
        # Force it explicitly and flush so the stored column is updated right away.
        # pylint: disable=no-search-all
        orders = (
            self.env["sale.order"].sudo().with_context(active_test=False).search([])
        )
        orders.invalidate_recordset(["amount_multicompany_reporting_currency"])
        orders._compute_amount_multicompany_reporting_currency()
        orders.flush_recordset(["amount_multicompany_reporting_currency"])
