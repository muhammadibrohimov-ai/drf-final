from django.urls import path, include
from .views import (
    CustomTokenObtainView,
    HomeView,
    PersonalPostsView,
    PersonalPostDetailView
)

from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", PersonalPostsView.as_view(), name='posts'),
    path("posts/<int:pk>/", PersonalPostDetailView.as_view(), name='posts-detail'),
    path("api/", SpectacularAPIView.as_view(), name="schema"),
    path("api/swagger/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(), name="redoc-ui"),
    path('auth/token/', CustomTokenObtainView.as_view(), name='token'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
