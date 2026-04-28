import requests
import logging
from .models import TelegramConfig

logger = logging.getLogger(__name__)

class TelegramService:
    """Servicio para enviar notificaciones a Telegram"""
    
    def __init__(self):
        self.config = None
        self._load_config()
        
    def _load_config(self):
        try:
            self.config, _ = TelegramConfig.objects.get_or_create(id=1)
        except Exception as e:
            logger.error(f"Error cargando configuración de Telegram: {e}")
            
    def send_message(self, message):
        """Enviar un mensaje simple"""
        if not self.config or not self.config.enabled:
            return False
            
        if not self.config.bot_token or not self.config.chat_id:
            logger.warning("Telegram habilitado pero falta Token o Chat ID")
            return False
            
        url = f"https://api.telegram.org/bot{self.config.bot_token}/sendMessage"
        payload = {
            'chat_id': self.config.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error enviando mensaje a Telegram: {e}")
            return False
            
    def send_signal_notification(self, signal):
        """Enviar notificación formateada de una señal de trading"""
        if not self.config or not self.config.enabled:
            return False
            
        emoji_dir = "📈 ALZA" if signal.signal_type == 'BREAKOUT_UP' else "📉 BAJA"
        
        # Formatear la hora
        hora_formateada = signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        message = (
            f"🚨 <b>RUPTURA DETECTADA (5 VELAS)</b> 🚨\n\n"
            f"<b>Activo:</b> {signal.symbol.name}\n"
            f"<b>Tipo:</b> {emoji_dir}\n"
            f"<b>Precio actual:</b> ${signal.price:.5f}\n"
            f"<b>Máx/Mín (5v):</b> ${signal.breakout_level:.5f}\n"
            f"<b>Filtro EMA 200:</b> ✅ Confirmado\n"
            f"<b>Hora:</b> {hora_formateada}"
        )
        
        return self.send_message(message)
