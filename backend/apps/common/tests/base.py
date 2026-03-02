from rest_framework.test import APITestCase
from django.test import TestCase
from .factories import UserFactory


class AuthenticatedAPITestCase(APITestCase):
    """
    Base class for authenticated API tests.
    Automatically creates a user and authenticates the client.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)


class OwnedModelTestMixin:
    """
    Mixin for testing OwnedModel multi-tenancy isolation.
    Use with TestCase or APITestCase.
    """

    def create_other_user(self):
        """Helper to create a second user for isolation tests"""
        return UserFactory.create()

    def assert_user_isolation(self, model_class, user1, user2, **create_kwargs):
        """
        Test that users can only see their own data.
        
        Args:
            model_class: The model class to test
            user1: First user
            user2: Second user
            **create_kwargs: Additional fields needed to create the model
        """
        obj1 = model_class.objects.create(created_by=user1, **create_kwargs)
        obj2 = model_class.objects.create(created_by=user2, **create_kwargs)

        user1_qs = model_class.objects.filter(created_by=user1)
        user2_qs = model_class.objects.filter(created_by=user2)

        self.assertIn(obj1, user1_qs)
        self.assertNotIn(obj2, user1_qs)
        self.assertIn(obj2, user2_qs)
        self.assertNotIn(obj1, user2_qs)
