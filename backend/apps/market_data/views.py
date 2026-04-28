from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from .models import Symbol, MarketData, TradingSignal, SystemStatus
from apps.analysis.models import TelegramConfig
from .serializers import SymbolSerializer, MarketDataSerializer, TradingSignalSerializer
import logging

logger = logging.getLogger(__name__)


class SymbolViewSet(viewsets.ModelViewSet):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Activar/desactivar un símbolo"""
        symbol = self.get_object()
        symbol.active = not symbol.active
        symbol.save()
        
        # Enviar notificación a Telegram
        try:
            from apps.analysis.telegram_service import TelegramService
            tg_service = TelegramService()
            status_text = "✅ ACTIVADO" if symbol.active else "❌ DESACTIVADO"
            message = (
                f"⚙️ <b>GESTIÓN DE ACTIVOS</b> ⚙️\n\n"
                f"<b>Activo:</b> {symbol.description}\n"
                f"<b>Ticker:</b> {symbol.name}\n"
                f"<b>Familia:</b> {symbol.category}\n"
                f"<b>Estado:</b> {status_text}"
            )
            tg_service.send_message(message)
        except Exception as e:
            logger.error(f"Error enviando notificación de toggle a Telegram: {e}")
            
        return Response({
            'id': symbol.id,
            'name': symbol.name,
            'active': symbol.active
        })


class MarketDataViewSet(viewsets.ModelViewSet):
    queryset = MarketData.objects.select_related('symbol').order_by('-timestamp')
    serializer_class = MarketDataSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Obtener los últimos datos de mercado"""
        symbol = request.query_params.get('symbol')
        timeframe = request.query_params.get('timeframe', 'H1')
        limit = int(request.query_params.get('limit', 100))

        queryset = self.queryset
        if symbol:
            queryset = queryset.filter(symbol__name=symbol)
        if timeframe:
            queryset = queryset.filter(timeframe=timeframe)

        latest_data = queryset[:limit]
        serializer = self.get_serializer(latest_data, many=True)
        return Response(serializer.data)


class TradingSignalViewSet(viewsets.ModelViewSet):
    queryset = TradingSignal.objects.select_related('symbol').order_by('-timestamp')
    serializer_class = TradingSignalSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener señales activas"""
        active_signals = self.queryset.filter(active=True)
        serializer = self.get_serializer(active_signals, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def dashboard_view(request):
    """Endpoint consolidado para el dashboard principal"""
    # Contadores
    total_symbols = Symbol.objects.count()
    active_symbols = Symbol.objects.filter(active=True).count()

    # Obtener latido del monitor
    monitor_status = SystemStatus.objects.filter(key='monitor_last_heartbeat').first()
    last_heartbeat = monitor_status.last_update if monitor_status else None

    # Obtener estado de Telegram
    tg_config, _ = TelegramConfig.objects.get_or_create(id=1)
    telegram_enabled = tg_config.enabled

    breakout_signals = TradingSignal.objects.filter(
        signal_type__in=['BREAKOUT_UP', 'BREAKOUT_DOWN'],
        active=True,
        symbol__active=True
    )
    total_breakouts = breakout_signals.count()
    bullish_breakouts = breakout_signals.filter(signal_type='BREAKOUT_UP').count()
    bearish_breakouts = breakout_signals.filter(signal_type='BREAKOUT_DOWN').count()

    # Rupturas recientes (últimas 10)
    recent_breakouts = TradingSignal.objects.filter(
        signal_type__in=['BREAKOUT_UP', 'BREAKOUT_DOWN'],
        active=True,
        symbol__active=True
    ).select_related('symbol').order_by('-updated_at')[:50]

    breakouts_data = []
    for signal in recent_breakouts:
        # Obtener la última vela H1 para datos de precio
        last_candle = MarketData.objects.filter(
            symbol=signal.symbol,
            timeframe='H1'
        ).order_by('-timestamp').first()

        breakouts_data.append({
            'id': signal.id,
            'symbol_name': signal.symbol.name,
            'signal_type': signal.signal_type,
            'price': float(signal.price) if signal.price else 0,
            'high_prev': float(last_candle.high_price) if last_candle else 0,
            'low_prev': float(last_candle.low_price) if last_candle else 0,
            'confidence': float(signal.confidence) if signal.confidence else 0,
            'timestamp': signal.timestamp,
            'updated_at': signal.updated_at,
            'description': signal.description,
        })

    # Lista de símbolos
    symbols = Symbol.objects.all().order_by('name')
    symbols_data = []
    for sym in symbols:
        symbols_data.append({
            'id': sym.id,
            'name': sym.name,
            'description': sym.description,
            'category': sym.category,
            'active': sym.active,
        })

    return Response({
        'stats': {
            'active_symbols': active_symbols,
            'total_symbols': total_symbols,
            'total_breakouts': total_breakouts,
            'bullish_breakouts': bullish_breakouts,
            'bearish_breakouts': bearish_breakouts,
            'last_heartbeat': last_heartbeat,
            'telegram_enabled': telegram_enabled,
        },
        'breakouts': breakouts_data,
        'symbols': symbols_data,
    })


@api_view(['POST'])
def analyze_all_view(request):
    """Ejecutar análisis de rupturas para todos los activos activos"""
    from apps.analysis.analysis_service import TechnicalAnalyzer
    analyzer = TechnicalAnalyzer()

    active_symbols = Symbol.objects.filter(active=True)
    results = []

    for symbol in active_symbols:
        try:
            result = analyzer.analyze_symbol(symbol.name, timeframe='H1')
            results.append({
                'symbol': symbol.name,
                'breakout_detected': result.get('breakout_detected', False) if result else False,
                'direction': result.get('breakout_direction') if result else None,
            })
        except Exception as e:
            logger.error(f"Error analizando {symbol.name}: {e}")
            results.append({
                'symbol': symbol.name,
                'error': str(e),
            })

    return Response({
        'analyzed': len(results),
        'results': results,
    })