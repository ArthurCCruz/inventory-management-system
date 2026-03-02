from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.common.tests import UserFactory


class AuthViewsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(username='testuser', password='testpass123')
        self.login_url = reverse('login')
        self.refresh_url = reverse('refresh')
        self.logout_url = reverse('logout')
        self.me_url = reverse('me')

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials returns access token and sets refresh cookie"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertIn('refresh_token', response.cookies)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials returns 401"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_login_with_missing_username(self):
        """Test login without username returns validation error"""
        data = {
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_login_with_missing_password(self):
        """Test login without password returns validation error"""
        data = {
            'username': 'testuser'
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_token_can_be_used_for_authenticated_requests(self):
        """Test that access token from login can be used for authenticated requests"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_refresh_with_valid_cookie(self):
        """Test refresh endpoint with valid refresh cookie returns new access token"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        
        self.client.cookies = login_response.cookies
        response = self.client.post(self.refresh_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_without_cookie(self):
        """Test refresh endpoint without refresh cookie returns 401"""
        response = self.client.post(self.refresh_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_refresh_with_invalid_token(self):
        """Test refresh endpoint with invalid token returns 401"""
        self.client.cookies['refresh_token'] = 'invalid_token'
        response = self.client.post(self.refresh_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_clears_refresh_cookie(self):
        """Test logout endpoint clears refresh cookie"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.client.cookies = login_response.cookies

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_logout_returns_success_message(self):
        """Test logout returns success message"""
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Logged out')

    def test_me_returns_authenticated_user_info(self):
        """Test me endpoint returns authenticated user info"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertIn('name', response.data)

    def test_me_unauthenticated_returns_401(self):
        """Test me endpoint without authentication returns 401"""
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
