from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TechnicalAnalysis, BreakoutAnalysis, TelegramConfig
from .serializers import TechnicalAnalysisSerializer, BreakoutAnalysisSerializer, TelegramConfigSerializer


class TechnicalAnalysisViewSet(viewsets.ModelViewSet):
    queryset = TechnicalAnalysis.objects.all()
    serializer_class = TechnicalAnalysisSerializer


class BreakoutAnalysisViewSet(viewsets.ModelViewSet):
    queryset = BreakoutAnalysis.objects.all()
    serializer_class = BreakoutAnalysisSerializer


class TelegramConfigViewSet(viewsets.ViewSet):
    """ViewSet para gestionar la configuración de Telegram (Singleton)"""
    
    def list(self, request):
        config, _ = TelegramConfig.objects.get_or_create(id=1)
        serializer = TelegramConfigSerializer(config)
        return Response(serializer.data)
    
    def create(self, request):
        config, _ = TelegramConfig.objects.get_or_create(id=1)
        serializer = TelegramConfigSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def test_message(self, request):
        """Enviar un mensaje de prueba para validar la configuración"""
        config, _ = TelegramConfig.objects.get_or_create(id=1)
        if not config.bot_token or not config.chat_id:
            return Response({'error': 'Token o Chat ID no configurados'}, status=status.HTTP_400_BAD_REQUEST)
        
        from .telegram_service import TelegramService
        service = TelegramService()
        success = service.send_message("🔔 Prueba de notificación de MT5 Market Data. ¡Configuración exitosa!")
        
        if success:
            return Response({'status': 'Mensaje de prueba enviado'})
        else:
            return Response({'error': 'Error enviando mensaje. Verifica el Token y Chat ID.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Activar o desactivar las notificaciones de Telegram"""
        config, _ = TelegramConfig.objects.get_or_create(id=1)
        config.enabled = not config.enabled
        config.save()
        return Response({
            'enabled': config.enabled,
            'status': 'Telegram ' + ('activado' if config.enabled else 'desactivado')
        })
