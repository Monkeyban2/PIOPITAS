#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "============================================"
    echo "  ERROR: No se encontró Python instalado."
    echo "  Descárgalo desde https://www.python.org/downloads/"
    echo "  (En Mac también puedes usar: brew install python)"
    echo "============================================"
    exit 1
fi

echo "============================================"
echo "  Instalando Piopitas..."
echo "============================================"

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations app_piopitas
python manage.py migrate
python manage.py poblar_menu
python manage.py crear_admin_demo

echo "============================================"
echo "  Listo. Abre http://127.0.0.1:8000 en tu navegador"
echo "  Panel admin: http://127.0.0.1:8000/inicioSA"
echo "  Correo: admin@piopitas.com"
echo "  Contraseña: Piopitas123"
echo "============================================"

python manage.py runserver
