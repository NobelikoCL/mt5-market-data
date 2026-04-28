# MT5 Market Data — Resumen de Reconstrucción Profesional

Este documento resume el estado actual del proyecto tras la reconstrucción total para convertirlo en un monitor de trading de alta fidelidad.

## 🚀 Estado Actual
El sistema ha sido profesionalizado con un enfoque en **Rupturas H1** y una interfaz de usuario estilo **Dark Mode Premium** (OKX Style).

### Características Implementadas:
- **Base de Datos Masiva:** 625 activos (Forex, Metales, Crypto, Acciones, Índices) con datos realistas y nombres profesionales (AAPL, BTCUSD, XAUUSD, etc.).
- **Motor de Análisis:** Detección automática de rupturas de máximos/mínimos H1 basada en las 4 velas anteriores cerradas, con filtro de confirmación EMA 200 (Solo compras sobre la EMA y ventas bajo la EMA).
- **Monitoreo Continuo:** Un script en segundo plano actualiza los precios y re-analiza todos los activos cada 1 minuto.
- **Dashboard de Alto Rendimiento:**
    - Visualización de estadísticas críticas en tiempo real.
    - Tabla de alertas de rupturas con niveles de confianza y precios exactos.
    - Buscador y selector de activos (Toggle ON/OFF) para monitorear solo lo que te interesa.
- **Infraestructura Simplificada:** Un solo `docker-compose.yml` y un script `start.sh` que lo hace todo.

## 🛠️ Arquitectura
- **Frontend:** React + Vite + Tailwind CSS (Diseño Custom Premium).
- **Backend:** Django 4.2 + Django Rest Framework (Endpoints optimizados).
- **Base de Datos:** PostgreSQL 15 (Persistencia total de señales y mercado).
- **Contenedores:** Dockerizado y orquestado.

## 📍 Accesos Rápidos
- **Frontend Dashboard:** [http://localhost:3003](http://localhost:3003)
- **Backend API:** [http://localhost:8001/api/](http://localhost:8001/api/)
- **API Dashboard Data:** [http://localhost:8001/api/market-data/dashboard/](http://localhost:8001/api/market-data/dashboard/)
- **Admin Django:** [http://localhost:8001/admin/](http://localhost:8001/admin/) (Usuario: `admin` / Pass: `admin`)

## ⚡ Comandos Útiles
Para reiniciar el sistema desde cero con datos nuevos y limpios:
```bash
./start.sh
```

Para ver los logs del backend:
```bash
docker compose logs -f backend
```

## 📝 Notas de Desarrollo
- La autenticación en la API ha sido desactivada temporalmente para facilitar el desarrollo rápido del frontend.
- El sistema utiliza un volumen llamado `mt5_data` para que tus activos y configuraciones no se pierdan al apagar la computadora.

---
*Generado automáticamente el 27 de abril de 2026.*
