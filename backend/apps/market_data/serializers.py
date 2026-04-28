from rest_framework import serializers
from .models import Symbol, MarketData, TradingSignal


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = '__all__'


class MarketDataSerializer(serializers.ModelSerializer):
    symbol_name = serializers.CharField(source='symbol.name', read_only=True)
    
    class Meta:
        model = MarketData
        fields = '__all__'


class TradingSignalSerializer(serializers.ModelSerializer):
    symbol_name = serializers.CharField(source='symbol.name', read_only=True)
    
    class Meta:
        model = TradingSignal
        fields = '__all__'