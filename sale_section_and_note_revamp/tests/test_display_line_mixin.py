# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged

from .common import TestDisplayLineMixinCommon


@tagged("post_install", "-at_install")
class TestDisplayLineMixin(TestDisplayLineMixinCommon):
    def test_01_is_section(self):
        self.assertTrue(self.sol_section_1.is_section())
        self.assertFalse(self.sol_product_order.is_section())

    def test_02_is_note(self):
        self.assertTrue(self.sol_note_1.is_note())
        self.assertFalse(self.sol_serv_deliver.is_note())

    def test_03_get_section(self):
        section = self.sol_product_order.get_section()
        self.assertEqual(section, self.sol_section_1)

    def test_04_get_note(self):
        note = self.sol_serv_deliver.get_note()
        self.assertEqual(note, self.sol_note_1)

    def test_05_get_section_subtotal(self):
        section_subtotal = self.sol_section_1.get_section_subtotal(
            fields=["price_total"]
        )
        expected_subtotal = sum(
            [
                self.sol_product_order.price_total,
                self.sol_serv_deliver.price_total,
                self.sol_serv_order.price_total,
            ]
        )
        # Check if the calculated subtotal matches the expected subtotal
        self.assertEqual(section_subtotal["price_total"], expected_subtotal)

    def test_06_prepare_section_or_note_values(self):
        with self.assertRaises(NotImplementedError):
            self.sol_product_order.prepare_section_or_note_values(self.sol_section_1)

    def test_07_inject_sections_and_notes(self):
        with self.assertRaises(NotImplementedError):
            self.sol_product_order.inject_sections_and_notes()
