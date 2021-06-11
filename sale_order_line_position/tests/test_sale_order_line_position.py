# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SingleTransactionCase


class TestSaleOrderLinePosition(SingleTransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_9")
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id})

    def test_new_line_position(self):
        line1 = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
                "product_uom_qty": 3.0,
            }
        )
        self.assertEqual(line1.position, 1)
        lines = self.env["sale.order.line"].create(
            [
                {
                    "order_id": self.order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "product_uom_qty": 5.0,
                },
                {
                    "order_id": self.order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "product_uom_qty": 9.0,
                },
            ]
        )
        self.assertEqual(lines[0].position, 2)
        self.assertEqual(lines[1].position, 3)

    def test_unlink_line(self):
        self.order.order_line[0].unlink()
        self.assertEqual(len(self.order.order_line), 2)
        self.assertEqual(self.order.order_line[0].position, 1)
        self.assertEqual(self.order.order_line[1].position, 2)
