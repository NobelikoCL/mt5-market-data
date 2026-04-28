import os
import django
import sys
from decimal import Decimal

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from apps.market_data.models import Symbol, TradingSignal
from apps.analysis.telegram_service import TelegramService

def send_example():
    # Obtener un símbolo para el ejemplo
    symbol = Symbol.objects.filter(name='AAPL').first() or Symbol.objects.first()
    
    if not symbol:
        print("No hay símbolos en la base de datos")
        return

    # Crear una señal ficticia (no se guarda en DB para no ensuciar)
    dummy_signal = TradingSignal(
        symbol=symbol,
        signal_type='BREAKOUT_UP',
        price=Decimal('185.49'),
        breakout_level=Decimal('185.40'),
        timestamp=timezone.now(),
        active=True,
        confidence=95,
        description="Señal de prueba"
    )
    
    tg = TelegramService()
    success = tg.send_signal_notification(dummy_signal)
    
    if success:
        print("✅ Ejemplo enviado correctamente a Telegram")
    else:
        print("❌ Error al enviar el ejemplo (¿Bot configurado?)")

if __name__ == '__main__':
    send_example()
