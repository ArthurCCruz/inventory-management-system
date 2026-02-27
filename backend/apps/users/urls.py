from django.urls import path
from .views import SignupView

urlpatterns = [
    path("users/", SignupView.as_view(), name="signup"),
]