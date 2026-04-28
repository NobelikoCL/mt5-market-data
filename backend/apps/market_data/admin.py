from django.contrib import admin
from .models import Symbol, MarketData, TradingSignal

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'active', 'created_at']
    list_filter = ['category', 'active']
    search_fields = ['name', 'description']

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'timeframe', 'timestamp', 'close_price', 'volume']
    list_filter = ['timeframe', 'symbol']
    search_fields = ['symbol__name']
    date_hierarchy = 'timestamp'

@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'timeframe', 'signal_type', 'timestamp', 'confidence', 'active']
    list_filter = ['signal_type', 'timeframe', 'active']
    search_fields = ['symbol__name']
    date_hierarchy = 'timestamp'