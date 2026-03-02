from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupViewTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')

    def test_signup_with_valid_data(self):
        """Test signup with valid data creates user"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertNotIn('password', response.data)

    def test_signup_with_duplicate_username_fails(self):
        """Test signup with duplicate username fails"""
        User.objects.create_user(username='existinguser', password='pass123')
        
        data = {
            'username': 'existinguser',
            'password': 'newpass123'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_signup_with_missing_username_fails(self):
        """Test signup without username fails"""
        data = {
            'password': 'testpass123'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_signup_with_missing_password_fails(self):
        """Test signup without password fails"""
        data = {
            'username': 'newuser'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_password_is_hashed(self):
        """Test that password is hashed, not stored in plain text"""
        data = {
            'username': 'newuser',
            'password': 'plainpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='newuser')
        self.assertNotEqual(user.password, 'plainpassword123')
        self.assertTrue(user.check_password('plainpassword123'))

    def test_password_not_returned_in_response(self):
        """Test that password field is not returned in response"""
        data = {
            'username': 'newuser',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)

    def test_signup_with_optional_fields(self):
        """Test signup with optional first_name and last_name"""
        data = {
            'username': 'newuser',
            'password': 'testpass123',
            'first_name': 'First',
            'last_name': 'Last'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='newuser')
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.last_name, 'Last')
