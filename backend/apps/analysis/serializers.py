from rest_framework import serializers
from .models import TechnicalAnalysis, BreakoutAnalysis, TelegramConfig


class TechnicalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalAnalysis
        fields = '__all__'


class BreakoutAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakoutAnalysis
        fields = '__all__'


class TelegramConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramConfig
        fields = '__all__'
