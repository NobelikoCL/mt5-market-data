from django.contrib import admin
from .models import TechnicalAnalysis, BreakoutAnalysis

@admin.register(TechnicalAnalysis)
class TechnicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'timeframe', 'timestamp', 'trend_direction', 'recommendation']
    list_filter = ['timeframe', 'trend_direction', 'recommendation']
    search_fields = ['symbol__name']
    date_hierarchy = 'timestamp'

@admin.register(BreakoutAnalysis)
class BreakoutAnalysisAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'timeframe', 'breakout_type', 'breakout_direction', 'is_valid']
    list_filter = ['timeframe', 'breakout_type', 'breakout_direction', 'is_valid']
    search_fields = ['symbol__name']
    date_hierarchy = 'analysis_timestamp'