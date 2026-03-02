from decimal import Decimal
from rest_framework import status
from django.urls import reverse
from apps.purchase_orders.models import PurchaseOrder
from apps.stock.models import StockMove
from apps.common.tests import AuthenticatedAPITestCase, UserFactory, ProductFactory, PurchaseOrderFactory


class PurchaseOrderViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.product = ProductFactory.create(created_by=self.user)
        self.po = PurchaseOrderFactory.create(created_by=self.user)
        self.list_url = reverse('purchaseorder-list')

    def test_list_returns_users_orders_only(self):
        """Test that list returns only user's orders"""
        other_user = UserFactory.create()
        PurchaseOrderFactory.create(created_by=other_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.po.id)

    def test_list_filtering_by_status(self):
        """Test that filtering by status works"""
        po_draft = PurchaseOrderFactory.create(
            created_by=self.user,
            status=PurchaseOrder.Status.DRAFT
        )
        po_confirmed = PurchaseOrderFactory.create(
            created_by=self.user,
            status=PurchaseOrder.Status.CONFIRMED
        )

        response = self.client.get(self.list_url, {'status': 'draft'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        statuses = [item['status'] for item in response.data]
        self.assertIn('draft', statuses)

    def test_list_ordering_by_created_at(self):
        """Test that ordering by created_at works"""
        response = self.client.get(self.list_url, {'ordering': '-created_at'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_with_lines(self):
        """Test creating order with lines"""
        data = {
            'supplier_name': 'Test Supplier',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '5.50'
                }
            ]
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)
        created_po = PurchaseOrder.objects.get(id=response.data['id'])
        self.assertEqual(created_po.lines.count(), 1)
        self.assertEqual(created_po.total_price, Decimal('55.00'))

    def test_create_with_empty_lines_fails(self):
        """Test that creating order with empty lines array fails"""
        data = {
            'supplier_name': 'Test Supplier',
            'lines': []
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_calculates_total_price_correctly(self):
        """Test that total_price is calculated correctly on create"""
        data = {
            'supplier_name': 'Test Supplier',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '10',
                    'unit_price': '5.00'
                },
                {
                    'product': self.product.id,
                    'quantity': '20',
                    'unit_price': '3.00'
                }
            ]
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_po = PurchaseOrder.objects.get(id=response.data['id'])
        self.assertEqual(created_po.total_price, Decimal('110.00'))

    def test_create_with_other_users_product_fails(self):
        """Test that using other user's product fails"""
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)

        data = {
            'supplier_name': 'Test Supplier',
            'lines': [
                {
                    'product': other_product.id,
                    'quantity': '10',
                    'unit_price': '5.00'
                }
            ]
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_order_with_lines(self):
        """Test retrieving order returns order with lines"""
        from apps.purchase_orders.models import PurchaseOrderLine
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('10'),
            unit_price=Decimal('5'),
            total_price=Decimal('50')
        )

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('lines', response.data)
        self.assertEqual(len(response.data['lines']), 1)

    def test_cannot_retrieve_other_users_order(self):
        """Test that user cannot retrieve other user's order"""
        other_user = UserFactory.create()
        other_po = PurchaseOrderFactory.create(created_by=other_user)

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': other_po.pk})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_draft_order(self):
        """Test updating draft order"""
        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        data = {
            'supplier_name': 'Updated Supplier',
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '15',
                    'unit_price': '7.00'
                }
            ]
        }
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.supplier_name, 'Updated Supplier')

    def test_cannot_update_confirmed_order(self):
        """Test that cannot update confirmed order"""
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        data = {'supplier_name': 'New Name'}
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_received_order(self):
        """Test that cannot update received order"""
        self.po.status = PurchaseOrder.Status.RECEIVED
        self.po.save()

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        data = {'supplier_name': 'New Name'}
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_recalculates_total_on_line_changes(self):
        """Test that update recalculates total on line changes"""
        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        data = {
            'lines': [
                {
                    'product': self.product.id,
                    'quantity': '25',
                    'unit_price': '4.00'
                }
            ]
        }
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.total_price, Decimal('100.00'))

    def test_cannot_update_other_users_order(self):
        """Test that user cannot update other user's order"""
        other_user = UserFactory.create()
        other_po = PurchaseOrderFactory.create(created_by=other_user)

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': other_po.pk})
        data = {'supplier_name': 'Hacked Name'}
        response = self.client.patch(detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_draft_order(self):
        """Test deleting draft order"""
        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PurchaseOrder.objects.filter(id=self.po.id).exists())

    def test_cannot_delete_confirmed_order(self):
        """Test that cannot delete confirmed order"""
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_received_order(self):
        """Test that cannot delete received order"""
        self.po.status = PurchaseOrder.Status.RECEIVED
        self.po.save()

        detail_url = reverse('purchaseorder-detail', kwargs={'pk': self.po.pk})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_draft_order(self):
        """Test confirming draft order"""
        from apps.purchase_orders.models import PurchaseOrderLine
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        confirm_url = reverse('purchaseorder-confirm', kwargs={'pk': self.po.pk})
        response = self.client.patch(confirm_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.status, PurchaseOrder.Status.CONFIRMED)

    def test_cannot_confirm_non_draft_order(self):
        """Test that cannot confirm non-draft order"""
        from apps.purchase_orders.models import PurchaseOrderLine
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()

        confirm_url = reverse('purchaseorder-confirm', kwargs={'pk': self.po.pk})
        response = self.client.patch(confirm_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_creates_pending_stock_moves(self):
        """Test that confirm creates pending stock moves"""
        from apps.purchase_orders.models import PurchaseOrderLine
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )

        initial_move_count = StockMove.objects.count()
        
        confirm_url = reverse('purchaseorder-confirm', kwargs={'pk': self.po.pk})
        response = self.client.patch(confirm_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StockMove.objects.count(), initial_move_count + 1)

    def test_receive_confirmed_order(self):
        """Test receiving confirmed order"""
        from apps.purchase_orders.models import PurchaseOrderLine
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            purchase_order_line=self.po.lines.first(),
            created_by=self.user
        )

        receive_url = reverse('purchaseorder-receive', kwargs={'pk': self.po.pk})
        response = self.client.patch(receive_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.status, PurchaseOrder.Status.RECEIVED)

    def test_cannot_receive_draft_order(self):
        """Test that cannot receive draft order"""
        receive_url = reverse('purchaseorder-receive', kwargs={'pk': self.po.pk})
        response = self.client.patch(receive_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_receive_creates_stock_lots(self):
        """Test that receive creates stock lots"""
        from apps.purchase_orders.models import PurchaseOrderLine
        from apps.stock.models import StockLot
        
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            purchase_order_line=self.po.lines.first(),
            created_by=self.user
        )

        initial_lot_count = StockLot.objects.count()

        receive_url = reverse('purchaseorder-receive', kwargs={'pk': self.po.pk})
        response = self.client.patch(receive_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(StockLot.objects.count(), initial_lot_count)

    def test_receive_moves_to_done_status(self):
        """Test that receive moves stock moves to DONE status"""
        from apps.purchase_orders.models import PurchaseOrderLine
        
        PurchaseOrderLine.objects.create(
            order=self.po,
            product=self.product,
            quantity=Decimal('100'),
            unit_price=Decimal('10'),
            total_price=Decimal('1000')
        )
        self.po.status = PurchaseOrder.Status.CONFIRMED
        self.po.save()
        
        move = StockMove.objects.create(
            product=self.product,
            quantity=Decimal('100'),
            from_location=StockMove.Location.SUPPLIER,
            to_location=StockMove.Location.STOCK,
            status=StockMove.Status.PENDING,
            purchase_order_line=self.po.lines.first(),
            created_by=self.user
        )

        receive_url = reverse('purchaseorder-receive', kwargs={'pk': self.po.pk})
        response = self.client.patch(receive_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        move.refresh_from_db()
        self.assertEqual(move.status, StockMove.Status.DONE)
