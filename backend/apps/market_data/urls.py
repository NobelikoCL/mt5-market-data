from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SymbolViewSet, MarketDataViewSet, TradingSignalViewSet, dashboard_view, analyze_all_view

router = DefaultRouter()
router.register(r'symbols', SymbolViewSet)
router.register(r'data', MarketDataViewSet)
router.register(r'signals', TradingSignalViewSet)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('analyze-all/', analyze_all_view, name='analyze-all'),
    path('', include(router.urls)),
]