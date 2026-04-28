#!/bin/bash

# Script para inicializar el sistema MT5 Market Data
cd /home/hernan/proyectos/desarrollo/mt5-market-data

echo "Iniciando servicios Docker..."
docker compose -f docker-compose.dev.yml up -d

# Esperar a que los servicios estén listos
echo "Esperando que los servicios estén listos..."
sleep 10

# Crear migraciones
echo "Creando migraciones..."
docker compose -f docker-compose.dev.yml exec backend python manage.py makemigrations

# Aplicar migraciones
echo "Aplicando migraciones..."
docker compose -f docker-compose.dev.yml exec backend python manage.py migrate

# Crear superusuario
echo "Creando superusuario..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mt5.com', '1234')" | docker compose -f docker-compose.dev.yml exec -T backend python manage.py shell

# Cargar datos de prueba
echo "Cargando datos de prueba..."
docker compose -f docker-compose.dev.yml exec backend python manage.py shell -c "
from apps.market_data.models import Symbol
from django.utils import timezone

# Crear símbolos básicos
symbols_data = [
    ('EURUSD', 'Euro Dólar Americano'),
    ('GBPUSD', 'Libra Esterlina Dólar Americano'),
    ('USDJPY', 'Dólar Americano Yen Japonés'),
]

for name, desc in symbols_data:
    Symbol.objects.get_or_create(name=name, defaults={'description': desc})
    print(f'Símbolo creado: {name}')

print('Sistema inicializado correctamente!')
"

echo "✅ Sistema MT5 Market Data inicializado correctamente!"
echo "🔗 URLs de acceso:"
echo "   - Backend Admin: http://localhost:8001/admin"
echo "   - Frontend: http://localhost:3000"
echo "   - Credenciales: admin / 1234"