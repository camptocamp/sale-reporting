# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


class TestDisplayLineMixinCommon(TestSaleCommon):

    def setUp(self):
        super().setUp()

        SaleOrder = self.env['sale.order'].with_context(tracking_disable=True)
        SaleOrderLine = self.env['sale.order.line'].with_context(
            tracking_disable=True
        )

        # create a generic Sale Order with all classical products and empty pricelist
        self.sale_order = SaleOrder.create({
            'partner_id': self.partner_a.id,
            'partner_invoice_id': self.partner_a.id,
            'partner_shipping_id': self.partner_a.id,
            'pricelist_id': self.company_data['default_pricelist'].id,
        })

        self.sol_section_1 = SaleOrderLine.create({
            'sequence': 1,
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Sample Section',
        })
        self.sol_product_order = SaleOrderLine.create({
            'sequence': 2,
            'name': self.company_data['product_order_no'].name,
            'product_id': self.company_data['product_order_no'].id,
            'product_uom_qty': 2,
            'product_uom': self.company_data['product_order_no'].uom_id.id,
            'price_unit': self.company_data['product_order_no'].list_price,
            'order_id': self.sale_order.id,
            'tax_id': False,
        })
        self.sol_serv_deliver = SaleOrderLine.create({
            'sequence': 3,
            'name': self.company_data['product_service_delivery'].name,
            'product_id': self.company_data['product_service_delivery'].id,
            'product_uom_qty': 2,
            'product_uom': self.company_data['product_service_delivery'].uom_id.id,
            'price_unit': self.company_data['product_service_delivery'].list_price,
            'order_id': self.sale_order.id,
            'tax_id': False,
        })
        self.sol_note_1 = SaleOrderLine.create({
            'sequence': 4,
            'order_id': self.sale_order.id,
            'display_type': 'line_note',
            'name': 'Sample Note 1',
        })
        self.sol_serv_order = SaleOrderLine.create({
            'sequence': 5,
            'name': self.company_data['product_service_order'].name,
            'product_id': self.company_data['product_service_order'].id,
            'product_uom_qty': 2,
            'product_uom': self.company_data['product_service_order'].uom_id.id,
            'price_unit': self.company_data['product_service_order'].list_price,
            'order_id': self.sale_order.id,
            'tax_id': False,
        })
        self.sol_section_2 = SaleOrderLine.create({
            'sequence': 6,
            'order_id': self.sale_order.id,
            'display_type': 'line_section',
            'name': 'Sample Section 2',
        })
        self.sol_product_deliver = SaleOrderLine.create({
            'sequence': 7,
            'name': self.company_data['product_delivery_no'].name,
            'product_id': self.company_data['product_delivery_no'].id,
            'product_uom_qty': 2,
            'product_uom': self.company_data['product_delivery_no'].uom_id.id,
            'price_unit': self.company_data['product_delivery_no'].list_price,
            'order_id': self.sale_order.id,
            'tax_id': False,
        })
        self.sol_note_2 = SaleOrderLine.create({
            'sequence': 8,
            'order_id': self.sale_order.id,
            'display_type': 'line_note',
            'name': 'Sample Note 2',
        })
        # We need to force a write to process sectiosn and notes
        self.sale_order.write({})
