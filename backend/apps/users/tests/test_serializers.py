from django.test import TestCase
from apps.users.serializers import SignupSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializerTestCase(TestCase):
    def test_creates_user_with_hashed_password(self):
        """Test that serializer creates user with hashed password"""
        data = {
            'username': 'testuser',
            'password': 'plainpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = SignupSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertIsNotNone(user.id)
        self.assertNotEqual(user.password, 'plainpassword123')
        self.assertTrue(user.check_password('plainpassword123'))

    def test_optional_first_name_handled_correctly(self):
        """Test that optional first_name is handled correctly"""
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = SignupSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, 'Test')

    def test_optional_last_name_handled_correctly(self):
        """Test that optional last_name is handled correctly"""
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = SignupSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        self.assertEqual(user.last_name, 'User')

    def test_password_not_exposed_in_serialized_output(self):
        """Test that password is not exposed in serialized output"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        serializer = SignupSerializer(user)

        self.assertNotIn('password', serializer.data)
        self.assertIn('username', serializer.data)
