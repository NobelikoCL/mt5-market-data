#!/usr/bin/env python
import os
import django
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from apps.market_data.models import Symbol, MarketData, TradingSignal

def generate_realistic_candles(base_price, num_candles, volatility=0.002, trend=0.0):
    candles = []
    price = base_price
    for i in range(num_candles):
        change_pct = random.gauss(trend, volatility)
        open_price = price
        close_price = open_price * (1 + change_pct)
        intra_volatility = abs(change_pct) + random.uniform(0.0005, 0.002)
        high_price = max(open_price, close_price) * (1 + random.uniform(0, intra_volatility))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, intra_volatility))
        volume = random.randint(500, 50000)
        candles.append({
            'open': round(open_price, 5),
            'high': round(high_price, 5),
            'low': round(low_price, 5),
            'close': round(close_price, 5),
            'volume': volume,
        })
        price = close_price
    return candles

def create_data():
    ticker_names = {
        # Forex
        'EURUSD': 'Euro vs US Dollar', 'GBPUSD': 'Great Britain Pound vs US Dollar',
        'USDJPY': 'US Dollar vs Japanese Yen', 'USDCHF': 'US Dollar vs Swiss Franc',
        'AUDUSD': 'Australian Dollar vs US Dollar', 'NZDUSD': 'New Zealand Dollar vs US Dollar',
        'USDCAD': 'US Dollar vs Canadian Dollar', 'EURGBP': 'Euro vs Great Britain Pound',
        'EURJPY': 'Euro vs Japanese Yen', 'GBPJPY': 'Great Britain Pound vs Japanese Yen',
        # Indices
        'US30': 'Dow Jones Industrial Average', 'US500': 'S&P 500 Index', 'NAS100': 'Nasdaq 100 Index',
        'GER40': 'DAX 40 Germany Index', 'UK100': 'FTSE 100 United Kingdom', 'FRA40': 'CAC 40 France Index',
        'JPN225': 'Nikkei 225 Japan', 'ESP35': 'IBEX 35 Spain Index',
        # Metals
        'XAUUSD': 'Gold Spot / US Dollar', 'XAGUSD': 'Silver Spot / US Dollar',
        'XPTUSD': 'Platinum Spot / US Dollar', 'XPDUSD': 'Palladium Spot / US Dollar',
        # Crypto
        'BTCUSD': 'Bitcoin / US Dollar', 'ETHUSD': 'Ethereum / US Dollar',
        'SOLUSD': 'Solana / US Dollar', 'XRPUSD': 'Ripple / US Dollar',
        'ADAUSD': 'Cardano / US Dollar', 'DOTUSD': 'Polkadot / US Dollar',
        'DOGEUSD': 'Dogecoin / US Dollar', 'LINKUSD': 'Chainlink / US Dollar',
        # Stocks
        'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft Corporation', 'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.', 'TSLA': 'Tesla Inc.', 'NVDA': 'NVIDIA Corporation',
        'META': 'Meta Platforms Inc.', 'NFLX': 'Netflix Inc.', 'AMD': 'Advanced Micro Devices',
        'INTC': 'Intel Corporation', 'PYPL': 'PayPal Holdings', 'ADBE': 'Adobe Inc.',
        'CSCO': 'Cisco Systems', 'PEP': 'PepsiCo Inc.', 'COST': 'Costco Wholesale',
        'AVGO': 'Broadcom Inc.', 'QCOM': 'QUALCOMM Inc.', 'SBUX': 'Starbucks Corp.',
        'DIS': 'The Walt Disney Co.', 'JPM': 'JPMorgan Chase & Co.', 'BAC': 'Bank of America',
        'V': 'Visa Inc.', 'MA': 'Mastercard Inc.', 'BABA': 'Alibaba Group Holding',
        'NKE': 'NIKE Inc.', 'WMT': 'Walmart Inc.', 'KO': 'The Coca-Cola Company', 
        'PG': 'Procter & Gamble Co.', 'JNJ': 'Johnson & Johnson',
    }

    categories = {
        'Forex (Mayores)': ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD'],
        'Forex (Menores)': ['AUDUSD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY'],
        'Índices Bursátiles': ['US30', 'US500', 'NAS100', 'GER40', 'UK100', 'FRA40', 'JPN225', 'ESP35'],
        'Metales Preciosos': ['XAUUSD', 'XAGUSD', 'XPTUSD', 'XPDUSD'],
        'Criptomonedas': ['BTCUSD', 'ETHUSD', 'SOLUSD', 'XRPUSD', 'ADAUSD', 'DOTUSD', 'DOGEUSD', 'LINKUSD'],
        'Tecnología (USA)': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC', 'ADBE', 'AVGO', 'QCOM'],
        'Consumo (USA)': ['SBUX', 'DIS', 'PEP', 'COST', 'WMT', 'KO', 'PG', 'NKE'],
        'Finanzas (USA)': ['JPM', 'BAC', 'V', 'MA', 'AXP', 'GS', 'MS', 'C', 'WFC'],
        'Salud (USA)': ['JNJ', 'PFE', 'ABBV', 'MRK', 'LLY', 'BMY', 'UNH'],
    }

    symbols_config = []
    for cat, tickers in categories.items():
        for ticker in tickers:
            # Precios base realistas
            if ticker == 'EURUSD': base = 1.0850
            elif ticker == 'GBPUSD': base = 1.2640
            elif ticker == 'USDJPY': base = 150.20
            elif ticker == 'USDCHF': base = 0.8810
            elif ticker == 'USDCAD': base = 1.3520
            elif ticker == 'XAUUSD': base = 2035.50
            elif ticker == 'XAGUSD': base = 22.80
            elif ticker == 'BTCUSD': base = 51200.0
            elif ticker == 'ETHUSD': base = 2950.0
            elif ticker == 'US30': base = 39100.0
            elif ticker == 'US500': base = 5080.0
            elif ticker == 'NAS100': base = 17950.0
            elif ticker == 'GER40': base = 17400.0
            elif ticker == 'UK100': base = 7680.0
            elif ticker == 'FRA40': base = 7900.0
            elif ticker == 'JPN225': base = 39200.0
            elif ticker == 'ESP35': base = 10100.0
            elif ticker.endswith('USD'): base = random.uniform(1.0, 100.0)
            else: base = random.uniform(50.0, 500.0)

            symbols_config.append({
                'name': ticker,
                'description': ticker_names.get(ticker, f"{ticker} CFD"),
                'category': cat,
                'base': base,
                'vol': 0.0015
            })

    real_companies = [
        ('Goldman Sachs', 'Banca (USA)'), ('Morgan Stanley', 'Banca (USA)'), ('Citigroup', 'Banca (USA)'), ('Wells Fargo', 'Banca (USA)'),
        ('Boeing Co.', 'Industria (USA)'), ('Lockheed Martin', 'Industria (USA)'), ('General Electric', 'Industria (USA)'), ('Caterpillar', 'Industria (USA)'),
        ('Exxon Mobil', 'Energía (USA)'), ('Chevron Corp.', 'Energía (USA)'), ('Shell PLC', 'Energía (Europa)'), ('TotalEnergies', 'Energía (Europa)'),
        ('Pfizer Inc.', 'Salud (USA)'), ('Moderna Inc.', 'Salud (USA)'), ('AstraZeneca', 'Salud (Europa)'), ('Novartis', 'Salud (Europa)'),
        ('Toyota Motor', 'Automotriz (Asia)'), ('Volkswagen', 'Automotriz (Europa)'), ('Ford Motor', 'Automotriz (USA)'), ('General Motors', 'Automotriz (USA)'),
        ('Samsung Electronics', 'Tecnología (Asia)'), ('Sony Group', 'Tecnología (Asia)'), ('TSMC', 'Tecnología (Asia)'), ('ASML Holding', 'Tecnología (Europa)')
    ]
    
    suffixes = ['Group', 'Inc.', 'Corp.', 'Ltd.', 'Holdings']
    while len(symbols_config) < 625:
        base_name, base_cat = random.choice(real_companies)
        idx = len(symbols_config)
        description = f"{base_name} {random.choice(['Global', 'International', 'Partners', 'Systems'])} {random.choice(suffixes)}"
        ticker = f"{base_name[:3].upper()}{idx:02d}.CFD"
        symbols_config.append({
            'name': ticker,
            'description': description,
            'category': f"Acciones ({base_cat})",
            'base': random.uniform(10.0, 1500.0),
            'vol': random.uniform(0.001, 0.004)
        })

    print(f"📊 Poblando {len(symbols_config)} activos con nombres profesionales...")
    for i, cfg in enumerate(symbols_config):
        symbol, _ = Symbol.objects.get_or_create(
            name=cfg['name'],
            defaults={'description': cfg['description'], 'category': cfg['category'], 'active': i < 100}
        )
        if MarketData.objects.filter(symbol=symbol).count() < 100:
            candles = generate_realistic_candles(cfg['base'], 200, volatility=0.002)
            now = timezone.now()
            start_time = now - timedelta(hours=200)
            bulk_data = [MarketData(
                symbol=symbol, timeframe='H1', timestamp=start_time + timedelta(hours=j),
                open_price=Decimal(str(c['open'])), high_price=Decimal(str(c['high'])),
                low_price=Decimal(str(c['low'])), close_price=Decimal(str(c['close'])),
                volume=c['volume'],
            ) for j, c in enumerate(candles)]
            MarketData.objects.bulk_create(bulk_data, ignore_conflicts=True)

    print("\n🔍 Ejecutando análisis inicial...")
    from apps.analysis.analysis_service import TechnicalAnalyzer
    analyzer = TechnicalAnalyzer()
    for symbol in Symbol.objects.filter(active=True):
        analyzer.analyze_symbol(symbol.name, timeframe='H1')
    print(f"✅ Población completada.")

if __name__ == '__main__':
    create_data()
