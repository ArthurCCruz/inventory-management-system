from django.test import TestCase
from apps.auth.serializers import LoginSerializer


class LoginSerializerTestCase(TestCase):
    def test_valid_data_passes_validation(self):
        """Test that valid login data passes validation"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'testuser')
        self.assertEqual(serializer.validated_data['password'], 'testpass123')

    def test_missing_username_fails(self):
        """Test that missing username fails validation"""
        data = {
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_missing_password_fails(self):
        """Test that missing password fails validation"""
        data = {
            'username': 'testuser'
        }
        serializer = LoginSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_password_whitespace_preserved(self):
        """Test that password whitespace is preserved (trim_whitespace=False)"""
        data = {
            'username': 'testuser',
            'password': '  pass with spaces  '
        }
        serializer = LoginSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['password'], '  pass with spaces  ')
