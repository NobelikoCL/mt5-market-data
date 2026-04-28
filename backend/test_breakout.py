import os
import django
import sys
from datetime import datetime, timedelta
import random

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.market_data.models import Symbol, MarketData, TradingSignal
from apps.analysis.analysis_service import TechnicalAnalyzer

def test():
    symbol, _ = Symbol.objects.get_or_create(name='TEST_EURUSD', defaults={'category': 'Forex'})
    MarketData.objects.filter(symbol=symbol).delete()
    TradingSignal.objects.filter(symbol=symbol).delete()
    
    # Create 60 data points
    base_price = 1.1000
    current_time = datetime.now() - timedelta(hours=60)
    for i in range(60):
        # Create a breakout on the last candle
        if i == 59:
            close_price = base_price + 0.0500 # huge jump
        else:
            close_price = base_price + random.uniform(-0.0010, 0.0010)
            
        MarketData.objects.create(
            symbol=symbol,
            timeframe='H1',
            timestamp=current_time,
            open_price=base_price,
            high_price=max(base_price, close_price) + 0.0005,
            low_price=min(base_price, close_price) - 0.0005,
            close_price=close_price,
            volume=1000
        )
        base_price = close_price
        current_time += timedelta(hours=1)
        
    print("Market data created.")
    analyzer = TechnicalAnalyzer()
    res = analyzer.analyze_symbol(symbol.name, 'H1')
    print("Analysis Result:", res)
    
    signals = TradingSignal.objects.filter(symbol=symbol)
    print("Trading Signals found:", len(signals))
    for s in signals:
        print(s.signal_type, s.price, s.description)

test()
