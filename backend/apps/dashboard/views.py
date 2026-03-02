from typing import cast
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.dashboard.services import get_dashboard_data
from apps.users.models import User

class DashboardView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        data = get_dashboard_data(cast(User, request.user))
        return Response(status=status.HTTP_200_OK, data=data)
