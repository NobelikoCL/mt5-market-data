#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "🚀 MT5 Market Data System - Iniciando..."
echo ""

# Levantar contenedores
echo "📦 Levantando contenedores..."
docker compose up -d --build

echo "⏳ Esperando a que la base de datos esté lista..."
sleep 5

# Migraciones
echo "🗄️  Aplicando migraciones..."
docker compose exec backend python manage.py migrate --noinput

# Superusuario
echo "👤 Verificando superusuario..."
docker compose exec backend python manage.py createsuperuser --username admin --email admin@mt5.com --noinput 2>/dev/null || true

# Datos realistas
echo "📊 Verificando datos de mercado..."
docker compose exec backend python /app/scripts/populate_realistic.py

# Iniciar monitor de rupturas en segundo plano
echo "🔍 Iniciando monitor de rupturas (cada 1 minuto)..."
docker compose exec -d backend python /app/scripts/monitor_breakouts.py

echo ""
echo "==================================================="
echo "✅ Sistema iniciado exitosamente"
echo "🌐 Frontend:     http://localhost:3003"
echo "⚙️  Backend API:  http://localhost:8001/api/"
echo "📊 Dashboard:     http://localhost:8001/api/market-data/dashboard/"
echo "🔧 Admin Django:  http://localhost:8001/admin/"
echo "==================================================="
