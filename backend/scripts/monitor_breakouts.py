#!/usr/bin/env python
import os
import django
import sys
import time
import random
from datetime import datetime
from decimal import Decimal

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from apps.market_data.models import Symbol, MarketData, TradingSignal, SystemStatus
from apps.analysis.analysis_service import TechnicalAnalyzer

def monitor():
    print("🚀 Iniciando monitor de rupturas (cada 1 minuto)...")
    analyzer = TechnicalAnalyzer()
    
    while True:
        try:
            active_symbols = Symbol.objects.filter(active=True)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Analizando {active_symbols.count()} activos...")
            
            # Actualizar latido del sistema
            SystemStatus.objects.update_or_create(
                key='monitor_last_heartbeat',
                defaults={'value': 'active', 'last_update': timezone.now()}
            )
            
            signals_found = 0
            for symbol in active_symbols:
                # 1. Simular actualización de precio (opcional, para ver movimiento en dashboard)
                latest_data = MarketData.objects.filter(symbol=symbol, timeframe='H1').order_by('-timestamp').first()
                if latest_data:
                    # Simular un pequeño movimiento
                    change_pct = random.uniform(-0.0005, 0.0005)
                    new_close = float(latest_data.close_price) * (1 + change_pct)
                    latest_data.close_price = Decimal(str(round(new_close, 5)))
                    
                    if new_close > float(latest_data.high_price):
                        latest_data.high_price = Decimal(str(round(new_close, 5)))
                    if new_close < float(latest_data.low_price):
                        latest_data.low_price = Decimal(str(round(new_close, 5)))
                    
                    latest_data.save()
                
                # 2. Ejecutar análisis
                result = analyzer.analyze_symbol(symbol.name, timeframe='H1')
                
                if result and result.get('breakout_detected'):
                    signals_found += 1
            
            print(f"✅ Análisis completado. Señales detectadas: {signals_found}")
            
        except Exception as e:
            print(f"❌ Error en el ciclo de monitoreo: {e}")
            
        # Esperar 1 minuto
        time.sleep(60)

if __name__ == '__main__':
    monitor()
