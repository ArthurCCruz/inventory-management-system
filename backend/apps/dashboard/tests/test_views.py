from rest_framework import status
from django.urls import reverse
from apps.common.tests import AuthenticatedAPITestCase, UserFactory, ProductFactory


class DashboardViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.dashboard_url = reverse('dashboard')

    def test_returns_dashboard_data_for_authenticated_user(self):
        """Test that dashboard returns data for authenticated user"""
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('inventory', response.data)
        self.assertIn('orders', response.data)
        self.assertIn('financial', response.data)

    def test_unauthenticated_returns_401(self):
        """Test that unauthenticated request returns 401"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_all_sections(self):
        """Test that all expected sections are returned"""
        response = self.client.get(self.dashboard_url)

        self.assertIn('total_products', response.data['inventory'])
        self.assertIn('purchase_orders', response.data['orders'])
        self.assertIn('cogs', response.data['financial'])

    def test_only_includes_users_data(self):
        """Test that only user's data is included"""
        ProductFactory.create(created_by=self.user)
        
        other_user = UserFactory.create()
        ProductFactory.create(created_by=other_user)

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['inventory']['total_products'], 1)
