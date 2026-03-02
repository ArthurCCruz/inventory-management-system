from rest_framework import status
from django.urls import reverse
from apps.common.tests import AuthenticatedAPITestCase, UserFactory, ProductFactory


class OwnedModelViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse('product-list')

    def test_get_queryset_filters_by_created_by(self):
        """Test that get_queryset filters by created_by"""
        ProductFactory.create(created_by=self.user)
        other_user = UserFactory.create()
        ProductFactory.create(created_by=other_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['created_by']['id'], self.user.id)

    def test_perform_create_sets_created_by_to_request_user(self):
        """Test that perform_create sets created_by to request.user"""
        data = {
            'name': 'New Product',
            'sku': 'NEW-001',
            'description': 'Description',
            'unit': 'unit'
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from apps.products.models import Product
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.created_by, self.user)

    def test_requires_authentication(self):
        """Test that authentication is required"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_multi_tenancy_isolation(self):
        """Test multi-tenancy isolation"""
        my_product = ProductFactory.create(created_by=self.user)
        other_user = UserFactory.create()
        other_product = ProductFactory.create(created_by=other_user)

        detail_url = reverse('product-detail', kwargs={'pk': other_product.pk})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        my_detail_url = reverse('product-detail', kwargs={'pk': my_product.pk})
        my_response = self.client.get(my_detail_url)
        
        self.assertEqual(my_response.status_code, status.HTTP_200_OK)
