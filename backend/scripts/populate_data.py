#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba
"""
import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
import sys
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.market_data.models import Symbol, MarketData, TradingSignal

def create_sample_data():
    """Crear datos de prueba para el sistema"""
    
    # Crear símbolos de ejemplo
    symbols_data = [
        {'name': 'EURUSD', 'description': 'Euro vs Dólar Americano'},
        {'name': 'GBPUSD', 'description': 'Libra Esterlina vs Dólar Americano'},
        {'name': 'USDJPY', 'description': 'Dólar Americano vs Yen Japonés'},
        {'name': 'BTCUSD', 'description': 'Bitcoin vs Dólar Americano'},
        {'name': 'ETHUSD', 'description': 'Ethereum vs Dólar Americano'},
    ]
    
    symbols = []
    for symbol_info in symbols_data:
        symbol, created = Symbol.objects.get_or_create(
            name=symbol_info['name'],
            defaults={'description': symbol_info['description'], 'active': True}
        )
        symbols.append(symbol)
        print(f'Símbolo creado: {symbol.name}')
    
    # Crear datos de mercado históricos
    print("\nCreando datos de mercado...")
    for symbol in symbols:
        base_price = random.uniform(1.0, 100.0)
        current_time = datetime.now() - timedelta(days=30)
        
        for _ in range(100):  # 100 puntos de datos por símbolo
            open_price = base_price
            high_price = open_price + random.uniform(0.01, 0.5)
            low_price = open_price - random.uniform(0.01, 0.3)
            close_price = random.uniform(low_price, high_price)
            volume = random.randint(1000, 100000)
            
            MarketData.objects.create(
                symbol=symbol,
                timestamp=current_time,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume,
                timeframe='H1'
            )
            
            current_time += timedelta(hours=1)
            base_price = close_price  # El próximo precio abre donde cerró el anterior
    
    print("Datos de mercado creados")
    
    # Crear algunas señales de trading
    print("\nCreando señales de trading...")
    signal_types = ['BUY', 'SELL', 'HOLD']
    indicators_list = ['RSI', 'MACD', 'Bollinger Bands', 'Moving Average', 'Stochastic']
    
    for symbol in symbols:
        for _ in range(5):
            signal_type = random.choice(signal_types)
            strength = random.randint(1, 10)
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 24))
            indicators = random.sample(indicators_list, random.randint(1, 3))
            
            TradingSignal.objects.create(
                symbol=symbol,
                timestamp=timestamp,
                signal_type=signal_type,
                confidence=strength * 10.0,
                price_level=random.uniform(1.0, 100.0),
                timeframe='H1',
                indicators={'indicators': indicators},
                description=f"Señal {signal_type} generada automáticamente"
            )
    
    print("Señales de trading creadas")
    
    print("\n✅ Datos de prueba creados exitosamente!")
    print(f"- Símbolos: {len(symbols)}")
    print(f"- Datos de mercado: {MarketData.objects.count()}")
    print(f"- Señales de trading: {TradingSignal.objects.count()}")

if __name__ == '__main__':
    create_sample_data()