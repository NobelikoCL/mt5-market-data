from django.db import models
from apps.market_data.models import Symbol
from django.utils import timezone


class TechnicalAnalysis(models.Model):
    """Análisis técnico para símbolos y timeframes específicos"""
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    
    # Indicadores técnicos
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    macd = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    macd_signal = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    macd_histogram = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Bandas de Bollinger
    bollinger_upper = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    bollinger_middle = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    bollinger_lower = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    # Análisis de tendencia
    trend_direction = models.CharField(max_length=10, choices=[
        ('UP', 'Alcista'),
        ('DOWN', 'Bajista'),
        ('SIDEWAYS', 'Lateral')
    ], default='SIDEWAYS')
    
    # Detección de rupturas
    breakout_detected = models.BooleanField(default=False)
    breakout_type = models.CharField(max_length=20, choices=[
        ('SUPPORT', 'Soporte'),
        ('RESISTANCE', 'Resistencia'),
        ('TRENDLINE', 'Línea de Tendencia'),
        ('CHANNEL', 'Canal')
    ], null=True, blank=True)
    
    breakout_direction = models.CharField(max_length=10, choices=[
        ('UP', 'Ruptura Alcista'),
        ('DOWN', 'Ruptura Bajista')
    ], null=True, blank=True)
    
    # Recomendación
    recommendation = models.CharField(max_length=20, choices=[
        ('STRONG_BUY', 'Fuerte Compra'),
        ('BUY', 'Compra'),
        ('HOLD', 'Mantener'),
        ('SELL', 'Venta'),
        ('STRONG_SELL', 'Fuerte Venta')
    ])
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['symbol', 'timeframe', 'timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timeframe', 'timestamp']),
            models.Index(fields=['breakout_detected', 'recommendation']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} - {self.recommendation}"


class BreakoutAnalysis(models.Model):
    """Análisis específico de rupturas"""
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=10)
    analysis_timestamp = models.DateTimeField(default=timezone.now)
    
    # Información de la ruptura
    breakout_type = models.CharField(max_length=20, choices=[
        ('SUPPORT', 'Soporte'),
        ('RESISTANCE', 'Resistencia'),
        ('TRENDLINE', 'Línea de Tendencia'),
        ('CHANNEL', 'Canal')
    ])
    
    breakout_direction = models.CharField(max_length=10, choices=[
        ('UP', 'Ruptura Alcista'),
        ('DOWN', 'Ruptura Bajista')
    ])
    
    # Niveles de ruptura
    breakout_level = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    volume_spike = models.BooleanField(default=False)
    
    # Confirmación de la señal
    is_valid = models.BooleanField(default=False)
    confirmation_candles = models.IntegerField(default=0)
    
    # Señal de trading resultante
    trading_signal = models.CharField(max_length=20, choices=[
        ('BUY', 'Comprar'),
        ('SELL', 'Vender'),
        ('HOLD', 'Esperar'),
        ('NONE', 'Sin señal')
    ], default='NONE')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'timeframe', 'analysis_timestamp']),
            models.Index(fields=['breakout_type', 'breakout_direction']),
            models.Index(fields=['is_valid', 'trading_signal']),
        ]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} - {self.breakout_type} {self.breakout_direction}"
class TelegramConfig(models.Model):
    """Configuración para las notificaciones de Telegram"""
    bot_token = models.CharField(max_length=100, blank=True)
    chat_id = models.CharField(max_length=50, blank=True)
    enabled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Telegram Config ({'Activado' if self.enabled else 'Desactivado'})"

    class Meta:
        verbose_name = "Configuración de Telegram"
        verbose_name_plural = "Configuración de Telegram"
