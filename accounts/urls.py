from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
