# MT5 Market Data System

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

Sistema automatizado para obtener datos del mercado financiero desde MT5/Tickmill y encontrar oportunidades de entrada basadas en rupturas en timeframe H1.

## Características

- **Backend Django**: API REST para obtener datos de mercado y análisis técnico
- **Frontend React**: Visualización de datos y señales de trading
- **Docker**: Contenedores para desarrollo y producción
- **Automatización**: Extracción automática de datos desde Tickmill Web
- **Base de datos PostgreSQL**: Almacenamiento robusto de datos históricos

## Credenciales MT5

- **URL**: https://www.tickmill.com/trade
- **Usuario**: 25314638
- **Contraseña**: E$AJd3}3^;%F

## Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/NobelikoCL/mt5-market-data.git
cd mt5-market-data

# Iniciar con Docker (recomendado)
./start.sh

# O iniciar manualmente
docker-compose up -d
```

## Uso

1. **Dashboard principal**: http://localhost:3003
2. **API Backend**: http://localhost:8001
3. **Documentación API**: http://localhost:8001/api/schema/

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

## Desarrollo

Para desarrollo local:

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.