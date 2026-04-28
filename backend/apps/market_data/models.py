from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Symbol(models.Model):
    """Símbolos financieros disponibles en MT5"""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='Forex')  # Forex, Stocks, Crypto, etc.
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MarketData(models.Model):
    """Datos históricos de mercado"""
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=10)  # M1, M5, M15, M30, H1, H4, D1, W1, MN
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=15, decimal_places=5)
    high_price = models.DecimalField(max_digits=15, decimal_places=5)
    low_price = models.DecimalField(max_digits=15, decimal_places=5)
    close_price = models.DecimalField(max_digits=15, decimal_places=5)
    volume = models.BigIntegerField()
    
    # Indicadores técnicos
    rsi = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    macd = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    macd_signal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    macd_histogram = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    bollinger_upper = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    bollinger_lower = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['symbol', 'timeframe', 'timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timeframe', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} {self.timestamp}"


class TradingSignal(models.Model):
    """Señales de trading generadas por el análisis"""
    SIGNAL_TYPES = [
        ('BUY', 'Compra'),
        ('SELL', 'Venta'),
        ('BREAKOUT_UP', 'Ruptura Alcista'),
        ('BREAKOUT_DOWN', 'Ruptura Bajista'),
        ('CONSOLIDATION', 'Consolidación'),
        ('HOLD', 'Mantener'),
    ]

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=10)
    signal_type = models.CharField(max_length=20, choices=SIGNAL_TYPES)
    timestamp = models.DateTimeField()
    price = models.DecimalField(max_digits=15, decimal_places=5)
    
    # Información del análisis
    confidence = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100%
    description = models.TextField()
    
    # Parámetros de la ruptura
    breakout_level = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    volume_spike = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'timeframe', 'timestamp']),
            models.Index(fields=['signal_type', 'active']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} {self.signal_type} ({self.confidence}%)"


class SystemStatus(models.Model):
    """Estado global del sistema (ej. último latido del monitor)"""
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value} ({self.last_update})"

    class Meta:
        verbose_name = "Estado del Sistema"
        verbose_name_plural = "Estados del Sistema"