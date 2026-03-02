from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'Environment variables DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(
                f'Superuser "{username}" already exists. Skipping creation.'
            ))
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" created successfully!'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error creating superuser: {str(e)}'
            ))