# MT5 Market Data System

Sistema automatizado para obtener datos del mercado financiero desde MT5/Tickmill y encontrar oportunidades de entrada basadas en rupturas en timeframe H1.

## Características

- **Backend Django**: API REST para obtener datos de mercado y análisis técnico
- **Frontend React**: Visualización de datos y señales de trading
- **Docker**: Contenedores para desarrollo y producción
- **Automatización**: Extracción automática de datos desde Tickmill Web

## Credenciales MT5

- **URL**: https://www.tickmill.com/trade
- **Usuario**: 25314638
- **Contraseña**: E$AJd3}3^;%F

## Estructura del Proyecto

```
mt5-market-data/
├── backend/                 # Backend Django
│   ├── apps/
│   │   ├── market_data/     # Datos de mercado y MT5
│   │   └── analysis/        # Análisis técnico y señales
│   ├── core/               # Configuración Django
│   └── scripts/            # Scripts de automatización
├── frontend/               # Frontend React
│   └── src/
│       ├── pages/          # Páginas principales
│       ├── components/     # Componentes reutilizables
│       └── services/      # Servicios API
└── docker/                 # Configuración Docker
```

## Objetivo

Automatizar la obtención de datos de MT5 para detectar rupturas en timeframe H1 y generar señales de entrada automatizadas.

## Puertos

- **Backend Django**: 8001
- **Frontend React**: 3003
- **Base de datos**: 5435