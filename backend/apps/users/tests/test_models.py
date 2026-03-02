from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.common.tests import UserFactory

User = get_user_model()


class UserModelTestCase(TestCase):
    def test_user_creation_with_valid_data(self):
        """Test creating a user with valid data"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.is_active)

    def test_name_property_returns_full_name(self):
        """Test that name property returns full name"""
        user = UserFactory.create(first_name='John', last_name='Doe')

        self.assertEqual(user.name, 'John Doe')

    def test_name_property_handles_missing_first_name(self):
        """Test that name property handles missing first name"""
        user = UserFactory.create(first_name='', last_name='Doe')

        self.assertEqual(user.name, 'Doe')

    def test_name_property_handles_missing_last_name(self):
        """Test that name property handles missing last name"""
        user = UserFactory.create(first_name='John', last_name='')

        self.assertEqual(user.name, 'John')

    def test_name_property_handles_missing_both_names(self):
        """Test that name property handles missing both names"""
        user = UserFactory.create(first_name='', last_name='')

        self.assertEqual(user.name, '')

    def test_username_uniqueness_constraint(self):
        """Test that username must be unique"""
        User.objects.create_user(username='testuser', password='pass123')

        with self.assertRaises(Exception):
            User.objects.create_user(username='testuser', password='pass456')

    def test_password_is_hashed(self):
        """Test that password is hashed on save, not stored in plain text"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.assertNotEqual(user.password, 'testpass123')
        self.assertTrue(user.check_password('testpass123'))
