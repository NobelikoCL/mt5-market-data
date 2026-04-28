from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnicalAnalysisViewSet, BreakoutAnalysisViewSet, TelegramConfigViewSet

router = DefaultRouter()
router.register(r'technical', TechnicalAnalysisViewSet)
router.register(r'breakouts', BreakoutAnalysisViewSet)
router.register(r'telegram-config', TelegramConfigViewSet, basename='telegram-config')

urlpatterns = [
    path('', include(router.urls)),
]
