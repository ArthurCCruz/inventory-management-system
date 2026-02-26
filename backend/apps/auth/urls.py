from django.urls import path
from .views import login_view, refresh_view, logout_view, me_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('refresh/', refresh_view, name='refresh'),
    path('logout/', logout_view, name='logout'),
    path('me/', me_view, name='me'),
]