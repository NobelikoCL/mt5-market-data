import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class MT5WebScraper:
    """Servicio para extraer datos de mercado desde Tickmill Web MT5"""
    
    def __init__(self, username, password, headless=True):
        self.username = username
        self.password = password
        self.base_url = "https://www.tickmill.com/trade"
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Configurar el driver de Selenium"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def login(self):
        """Iniciar sesión en Tickmill"""
        try:
            logger.info("Iniciando sesión en Tickmill...")
            self.driver.get(self.base_url)
            
            # Esperar a que cargue la página de login
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "login-form"))
            )
            
            # Buscar campos de login
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Ingresar credenciales
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Hacer login
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_button.click()
            
            # Esperar a que cargue el dashboard
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "trading-view"))
            )
            
            logger.info("Login exitoso")
            return True
            
        except TimeoutException:
            logger.error("Timeout durante el login")
            return False
        except Exception as e:
            logger.error(f"Error durante login: {e}")
            return False
    
    def get_market_data(self, symbol, timeframe="H1", count=100):
        """Obtener datos de mercado para un símbolo específico"""
        try:
            # Navegar a la página del símbolo específico
            symbol_url = f"{self.base_url}/symbol/{symbol}"
            self.driver.get(symbol_url)
            
            # Esperar a que cargue el gráfico
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chart-container"))
            )
            
            # Cambiar timeframe si es necesario
            self.change_timeframe(timeframe)
            
            # Extraer datos del gráfico
            data = self.extract_chart_data(symbol, timeframe, count)
            
            return data
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de mercado: {e}")
            return None
    
    def change_timeframe(self, timeframe):
        """Cambiar el timeframe del gráfico"""
        try:
            # Buscar y hacer clic en el selector de timeframe
            timeframe_selector = self.driver.find_element(By.CLASS_NAME, "timeframe-selector")
            timeframe_selector.click()
            
            # Seleccionar el timeframe específico
            timeframe_option = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{timeframe}')]")
            timeframe_option.click()
            
            # Esperar a que se actualice el gráfico
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error cambiando timeframe: {e}")
    
    def extract_chart_data(self, symbol, timeframe, count):
        """Extraer datos del gráfico usando JavaScript"""
        try:
            # Ejecutar JavaScript para obtener datos del gráfico
            script = """
            if (typeof window.TradingView !== 'undefined' && window.TradingView.chart) {
                var chart = window.TradingView.chart();
                var data = chart.getVisibleRange();
                return {
                    symbol: chart.symbol(),
                    timeframe: chart.resolution(),
                    data: data
                };
            }
            return null;
            """
            
            result = self.driver.execute_script(script)
            
            if result:
                # Procesar los datos obtenidos
                processed_data = self.process_chart_data(result, symbol, timeframe)
                return processed_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error extrayendo datos del gráfico: {e}")
            return None
    
    def process_chart_data(self, raw_data, symbol, timeframe):
        """Procesar datos crudos del gráfico"""
        # Aquí procesaríamos los datos para convertirlos al formato de MarketData
        # Por ahora retornamos datos de ejemplo
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'data_points': raw_data.get('data', [])
        }
    
    def get_available_symbols(self):
        """Obtener lista de símbolos disponibles"""
        try:
            # Navegar a la página de símbolos
            symbols_url = f"{self.base_url}/symbols"
            self.driver.get(symbols_url)
            
            # Esperar a que cargue la lista
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "symbols-list"))
            )
            
            # Extraer símbolos
            symbols = []
            symbol_elements = self.driver.find_elements(By.CLASS_NAME, "symbol-item")
            
            for element in symbol_elements:
                symbol_name = element.find_element(By.CLASS_NAME, "symbol-name").text
                symbol_category = element.find_element(By.CLASS_NAME, "symbol-category").text
                
                symbols.append({
                    'name': symbol_name,
                    'category': symbol_category
                })
            
            return symbols
            
        except Exception as e:
            logger.error(f"Error obteniendo símbolos disponibles: {e}")
            return []
    
    def detect_breakouts(self, symbol, timeframe="H1"):
        """Detectar rupturas en el timeframe especificado"""
        try:
            # Obtener datos del mercado
            market_data = self.get_market_data(symbol, timeframe)
            
            if not market_data:
                return None
            
            # Análisis de rupturas (implementación básica)
            breakout_signals = self.analyze_breakouts(market_data)
            
            return breakout_signals
            
        except Exception as e:
            logger.error(f"Error detectando rupturas: {e}")
            return None
    
    def analyze_breakouts(self, market_data):
        """Analizar datos para detectar rupturas"""
        # Implementar lógica de análisis de rupturas
        # Por ahora retornamos señales de ejemplo
        return {
            'symbol': market_data['symbol'],
            'timeframe': market_data['timeframe'],
            'signals': [
                {
                    'type': 'BREAKOUT_UP',
                    'confidence': 75.5,
                    'price_level': 1.2345,
                    'description': 'Ruptura alcista detectada en H1'
                }
            ]
        }
    
    def close(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()


# Función principal para usar el servicio
def get_mt5_data(username, password, symbols=None, timeframes=None):
    """Función principal para obtener datos de MT5"""
    scraper = MT5WebScraper(username, password)
    
    try:
        scraper.setup_driver()
        
        if not scraper.login():
            return None
        
        # Si no se especifican símbolos, obtener todos los disponibles
        if not symbols:
            symbols_data = scraper.get_available_symbols()
            symbols = [s['name'] for s in symbols_data]
        
        # Si no se especifican timeframes, usar H1 como default
        if not timeframes:
            timeframes = ['H1']
        
        all_data = {}
        
        for symbol in symbols:
            all_data[symbol] = {}
            for timeframe in timeframes:
                data = scraper.get_market_data(symbol, timeframe)
                all_data[symbol][timeframe] = data
        
        return all_data
        
    finally:
        scraper.close()