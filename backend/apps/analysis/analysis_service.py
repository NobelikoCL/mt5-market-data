import pandas as pd
import numpy as np
# import talib
from datetime import datetime, timedelta
from apps.market_data.models import MarketData, Symbol
from .models import TechnicalAnalysis, BreakoutAnalysis
import logging

logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Analizador técnico para detectar rupturas en timeframe H1"""
    
    def __init__(self):
        self.min_data_points = 50  # Mínimo de datos para análisis
    
    def analyze_symbol(self, symbol_name, timeframe='H1', data_points=100):
        """Analizar un símbolo específico"""
        try:
            # Obtener datos históricos
            market_data = MarketData.objects.filter(
                symbol__name=symbol_name,
                timeframe=timeframe
            ).order_by('-timestamp')[:data_points]
            
            if len(market_data) < self.min_data_points:
                logger.warning(f"Datos insuficientes para {symbol_name}: {len(market_data)}")
                return None
            
            # Convertir a DataFrame
            df = self.prepare_dataframe(market_data)
            
            # Realizar análisis técnico
            analysis = self.perform_technical_analysis(df, symbol_name, timeframe)
            
            # Detectar rupturas
            breakout_analysis = self.detect_breakouts(df, symbol_name, timeframe)
            
            # Combinar resultados
            if analysis and breakout_analysis:
                analysis.update(breakout_analysis)
            
            # Guardar análisis
            if analysis:
                self.save_analysis(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando {symbol_name}: {e}")
            return None
    
    def prepare_dataframe(self, market_data):
        """Preparar DataFrame para análisis"""
        data = []
        
        for record in market_data:
            data.append({
                'timestamp': record.timestamp,
                'open': float(record.open_price),
                'high': float(record.high_price),
                'low': float(record.low_price),
                'close': float(record.close_price),
                'volume': float(record.volume)
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def perform_technical_analysis(self, df, symbol_name, timeframe):
        """Realizar análisis técnico completo"""
        try:
            # Calcular indicadores técnicos
            df = self.calculate_indicators(df)
            
            # Análisis de tendencia
            trend_analysis = self.analyze_trend(df)
            
            # Análisis de soporte y resistencia
            support_resistance = self.analyze_support_resistance(df)
            
            # Análisis de volumen
            volume_analysis = self.analyze_volume(df)
            
            # Recomendación basada en análisis
            recommendation = self.generate_recommendation(df, trend_analysis)
            
            # Últimos valores
            latest = df.iloc[-1]
            
            analysis = {
                'symbol': symbol_name,
                'timeframe': timeframe,
                'timestamp': latest['timestamp'],
                'current_price': latest['close'],
                'trend_direction': trend_analysis['direction'],
                'trend_strength': trend_analysis['strength'],
                'support_levels': support_resistance['support'],
                'resistance_levels': support_resistance['resistance'],
                'volume_trend': volume_analysis['trend'],
                'rsi_value': latest['rsi'] if 'rsi' in df.columns else None,
                'rsi_signal': self.get_rsi_signal(latest['rsi']) if 'rsi' in df.columns else None,
                'macd_value': latest['macd'] if 'macd' in df.columns else None,
                'macd_signal': self.get_macd_signal(latest['macd'], latest['macd_signal']) if 'macd' in df.columns else None,
                'recommendation': recommendation,
                'indicators': {
                    'rsi': latest['rsi'] if 'rsi' in df.columns else None,
                    'macd': latest['macd'] if 'macd' in df.columns else None,
                    'macd_signal': latest['macd_signal'] if 'macd_signal' in df.columns else None,
                    'bollinger_upper': latest['bb_upper'] if 'bb_upper' in df.columns else None,
                    'bollinger_lower': latest['bb_lower'] if 'bb_lower' in df.columns else None
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis técnico: {e}")
            return None
    
    def calculate_indicators(self, df):
        """Calcular indicadores técnicos básicos (sin TA-Lib por ahora)"""
        try:
            # RSI básico
            if len(df) >= 14:
                df['rsi'] = self.calculate_rsi(df['close'])
            
            # MACD básico
            if len(df) >= 26:
                df['macd'], df['macd_signal'] = self.calculate_macd(df['close'])
            
            # Bollinger Bands básicas
            if len(df) >= 20:
                df['bb_upper'], df['bb_lower'] = self.calculate_bollinger_bands(df['close'])
            
            # Media móvil simple
            if len(df) >= 20:
                df['sma_20'] = df['close'].rolling(window=20).mean()
            if len(df) >= 50:
                df['sma_50'] = df['close'].rolling(window=50).mean()
            
            # Media móvil exponencial 200 para filtro de confirmación
            if len(df) >= 200:
                df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
            elif len(df) > 0:
                # Si no hay suficientes datos para 200, usar lo que haya como aproximación
                df['ema_200'] = df['close'].ewm(span=len(df), adjust=False).mean()
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculando indicadores: {e}")
            return df
    
    def analyze_trend(self, df):
        """Analizar tendencia del mercado"""
        try:
            # Usar medias móviles para determinar tendencia
            if len(df) >= 50:
                sma_20 = df['sma_20'].iloc[-1]
                sma_50 = df['sma_50'].iloc[-1]
                current_price = df['close'].iloc[-1]
                
                # Determinar dirección de tendencia
                if sma_20 > sma_50 and current_price > sma_20:
                    direction = 'BULLISH'
                    strength = min(100, ((current_price - sma_20) / sma_20) * 1000)
                elif sma_20 < sma_50 and current_price < sma_20:
                    direction = 'BEARISH'
                    strength = min(100, ((sma_20 - current_price) / sma_20) * 1000)
                else:
                    direction = 'SIDEWAYS'
                    strength = 50.0
            else:
                direction = 'SIDEWAYS'
                strength = 50.0
            
            return {'direction': direction, 'strength': float(strength)}
            
        except Exception as e:
            logger.error(f"Error analizando tendencia: {e}")
            return {'direction': 'SIDEWAYS', 'strength': 50.0}
    
    def detect_breakouts(self, df, symbol_name, timeframe):
        """
        Detectar rupturas en el precio basado en la lógica:
        1. Revisar las 4 velas anteriores cerradas del activo (high y low).
        2. Si la vela actual rompe el high/low de esas 4 velas, hay señal.
        3. Filtro EMA 200: 
           - Si precio > EMA 200 y rompe High -> Ruptura confirmada (BUY).
           - Si precio < EMA 200 y rompe Low -> Ruptura confirmada (SELL).
        """
        try:
            if len(df) < 5:
                return {'breakout_detected': False}
            
            # La última vela es la "actual" (en formación o recién cerrada)
            # Las 5 anteriores son las velas cerradas de referencia
            current_candle = df.iloc[-1]
            previous_5_candles = df.iloc[-6:-1]
            
            high_5 = previous_5_candles['high'].max()
            low_5 = previous_5_candles['low'].min()
            
            ema_200 = current_candle.get('ema_200')
            if ema_200 is None:
                # Fallback si no hay EMA 200 calculada
                ema_200 = df['close'].mean()

            # Confirmación de ruptura por CIERRE (más conservador y preciso)
            breakout_up = current_candle['close'] > high_5
            breakout_down = current_candle['close'] < low_5
            
            confirmed_up = breakout_up and current_candle['close'] > ema_200
            confirmed_down = breakout_down and current_candle['close'] < ema_200
            
            if confirmed_up or confirmed_down:
                direction = 'UP' if confirmed_up else 'DOWN'
                
                # Nivel de confianza basado en la distancia del cierre al nivel roto
                if confirmed_up:
                    dist = (current_candle['close'] - high_5) / high_5
                else:
                    dist = (low_5 - current_candle['close']) / low_5
                
                confidence = min(95.0, 70.0 + (dist * 1000))
                
                # Guardar análisis de ruptura
                self.save_breakout_analysis(
                    symbol_name, timeframe, current_candle['timestamp'],
                    direction, confidence, current_candle['close']
                )

                # Generar TradingSignal para el dashboard
                try:
                    from apps.market_data.models import TradingSignal, Symbol
                    symbol_obj = Symbol.objects.get(name=symbol_name)
                    
                    signal_type = 'BREAKOUT_UP' if confirmed_up else 'BREAKOUT_DOWN'
                    
                    # 1. Ver si ya existe una señal activa para esta vela y misma dirección
                    existing_signal = TradingSignal.objects.filter(
                        symbol=symbol_obj,
                        timeframe=timeframe,
                        timestamp=current_candle['timestamp'],
                        signal_type=signal_type,
                        active=True
                    ).first()
                    
                    if existing_signal:
                        # Actualizar precio y confianza, NO enviar Telegram de nuevo
                        existing_signal.price = current_candle['close']
                        existing_signal.confidence = confidence
                        existing_signal.save()
                        logger.info(f"Señal actualizada para {symbol_name} (sin spam)")
                    else:
                        # Es una señal nueva o cambió la dirección
                        TradingSignal.objects.filter(
                            symbol=symbol_obj, 
                            timeframe=timeframe,
                            active=True
                        ).update(active=False)
                        
                        desc = f"Ruptura H1 confirmada: {'Alcista sobre EMA 200' if confirmed_up else 'Bajista bajo EMA 200'}"
                        
                        signal = TradingSignal.objects.create(
                            symbol=symbol_obj,
                            timeframe=timeframe,
                            timestamp=current_candle['timestamp'],
                            signal_type=signal_type,
                            price=current_candle['close'],
                            confidence=confidence,
                            description=desc,
                            breakout_level=high_5 if confirmed_up else low_5,
                            active=True
                        )
                        
                        logger.info(f"Nueva señal generada para {symbol_name}: {signal_type}")
                        
                        # Enviar notificación a Telegram SOLO si es nueva
                        try:
                            from .telegram_service import TelegramService
                            tg_service = TelegramService()
                            tg_service.send_signal_notification(signal)
                        except Exception as te:
                            logger.error(f"Error enviando notificación Telegram: {te}")
                    
                    return {
                        'breakout_detected': True,
                        'breakout_direction': direction,
                        'breakout_confidence': confidence,
                        'breakout_level': current_candle['close'],
                        'ema_200': ema_200
                    }
                    
                except Exception as e:
                    logger.error(f"Error gestionando TradingSignal para {symbol_name}: {e}")
            
            else:
                # No se detectó ruptura en este momento.
                # Si había una señal activa para ESTA vela, la desactivamos (Reversión)
                try:
                    from apps.market_data.models import TradingSignal, Symbol
                    symbol_obj = Symbol.objects.get(name=symbol_name)
                    
                    active_current_signal = TradingSignal.objects.filter(
                        symbol=symbol_obj,
                        timeframe=timeframe,
                        timestamp=current_candle['timestamp'],
                        active=True
                    )
                    if active_current_signal.exists():
                        active_current_signal.update(active=False)
                        logger.info(f"Señal desactivada por reversión en {symbol_name}")
                except Exception as e:
                    logger.error(f"Error desactivando señal por reversión: {e}")
            
            return {'breakout_detected': False}
            
        except Exception as e:
            logger.error(f"Error detectando rupturas: {e}")
            return {'breakout_detected': False}
    
    def detect_bb_breakout(self, df):
        """Detectar ruptura de Bandas de Bollinger"""
        try:
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            
            # Verificar si el precio salió de las bandas
            if latest['close'] > latest['bb_upper'] and previous['close'] <= previous['bb_upper']:
                return {'detected': True, 'confidence': 75.0, 'type': 'BB_UPPER'}
            elif latest['close'] < latest['bb_lower'] and previous['close'] >= previous['bb_lower']:
                return {'detected': True, 'confidence': 75.0, 'type': 'BB_LOWER'}
            
            return {'detected': False, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"Error detectando ruptura BB: {e}")
            return {'detected': False, 'confidence': 0.0}
    
    def detect_support_resistance_breakout(self, df):
        """Detectar ruptura de soporte/resistencia"""
        # Implementación básica - se puede mejorar
        try:
            latest = df.iloc[-1]
            
            # Calcular niveles de soporte/resistencia simples
            resistance = df['high'].tail(20).max()
            support = df['low'].tail(20).min()
            
            # Verificar ruptura
            if latest['close'] > resistance:
                return {'detected': True, 'confidence': 80.0, 'type': 'RESISTANCE'}
            elif latest['close'] < support:
                return {'detected': True, 'confidence': 80.0, 'type': 'SUPPORT'}
            
            return {'detected': False, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"Error detectando ruptura S/R: {e}")
            return {'detected': False, 'confidence': 0.0}
    
    def analyze_support_resistance(self, df):
        """Analizar niveles de soporte y resistencia"""
        # Implementación simplificada
        try:
            # Usar máximos y mínimos recientes
            support_levels = df['low'].tail(50).nsmallest(3).tolist()
            resistance_levels = df['high'].tail(50).nlargest(3).tolist()
            
            return {
                'support': sorted(support_levels),
                'resistance': sorted(resistance_levels, reverse=True)
            }
        except Exception as e:
            logger.error(f"Error analizando S/R: {e}")
            return {'support': [], 'resistance': []}
    
    def analyze_volume(self, df):
        """Analizar tendencia del volumen"""
        try:
            if len(df) < 5:
                return {'trend': 'STABLE'}
            
            # Calcular media móvil del volumen
            volume_ma = df['volume'].tail(5).mean()
            current_volume = df['volume'].iloc[-1]
            
            if current_volume > volume_ma * 1.2:
                trend = 'INCREASING'
            elif current_volume < volume_ma * 0.8:
                trend = 'DECREASING'
            else:
                trend = 'STABLE'
            
            return {'trend': trend}
            
        except Exception as e:
            logger.error(f"Error analizando volumen: {e}")
            return {'trend': 'STABLE'}
    
    def generate_recommendation(self, df, trend_analysis):
        """Generar recomendación de trading"""
        try:
            latest = df.iloc[-1]
            
            # Lógica básica de recomendación
            if trend_analysis['direction'] == 'BULLISH' and trend_analysis['strength'] > 70:
                return 'STRONG_BUY'
            elif trend_analysis['direction'] == 'BEARISH' and trend_analysis['strength'] > 70:
                return 'STRONG_SELL'
            elif trend_analysis['direction'] == 'BULLISH':
                return 'BUY'
            elif trend_analysis['direction'] == 'BEARISH':
                return 'SELL'
            else:
                return 'HOLD'
                
        except Exception as e:
            logger.error(f"Error generando recomendación: {e}")
            return 'HOLD'
    
    def get_rsi_signal(self, rsi_value):
        """Interpretar señal RSI"""
        if rsi_value is None:
            return None
        
        if rsi_value < 30:
            return 'OVERSOLD'
        elif rsi_value > 70:
            return 'OVERBOUGHT'
        else:
            return 'NEUTRAL'
    
    def calculate_rsi(self, prices, period=14):
        """Calcular RSI básico"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcular MACD básico"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calcular Bandas de Bollinger básicas"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, lower_band
    
    def get_macd_signal(self, macd, macd_signal):
        """Interpretar señal MACD"""
        if macd is None or macd_signal is None:
            return None
        
        if macd > macd_signal:
            return 'BULLISH'
        elif macd < macd_signal:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def save_analysis(self, analysis):
        """Guardar análisis técnico en la base de datos"""
        try:
            symbol = Symbol.objects.get(name=analysis['symbol'])
            
            TechnicalAnalysis.objects.create(
                symbol=symbol,
                timeframe=analysis['timeframe'],
                timestamp=analysis['timestamp'],
                trend_direction=analysis['trend_direction'],
                rsi=analysis['rsi_value'],
                macd=analysis['macd_value'],
                macd_signal=analysis['indicators']['macd_signal'] if analysis.get('indicators') else None,
                breakout_detected=analysis.get('breakout_detected', False),
                breakout_direction=analysis.get('breakout_direction', 'UP'),
                recommendation=analysis['recommendation']
            )
            
        except Exception as e:
            logger.error(f"Error guardando análisis: {e}")
    
    def save_breakout_analysis(self, symbol_name, timeframe, timestamp, direction, confidence, level):
        """Guardar análisis específico de ruptura"""
        try:
            symbol = Symbol.objects.get(name=symbol_name)
            
            BreakoutAnalysis.objects.create(
                symbol=symbol,
                timeframe=timeframe,
                analysis_timestamp=timestamp,
                breakout_type='RESISTANCE' if direction == 'UP' else 'SUPPORT',
                breakout_level=level,
                breakout_direction='UP' if direction == 'UP' else 'DOWN',
                volume_spike=False,
                confirmation_candles=1,
                is_valid=True,
                trading_signal='BUY' if direction == 'UP' else 'SELL'
            )
            
        except Exception as e:
            logger.error(f"Error guardando análisis de ruptura: {e}")