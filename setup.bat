@echo off
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ============================================
    echo   ERROR: No se encontro Python instalado.
    echo   Descargalo desde https://www.python.org/downloads/
    echo   IMPORTANTE: durante la instalacion, marca la
    echo   casilla "Add Python to PATH".
    echo ============================================
    pause
    exit /b 1
)

echo ============================================
echo   Instalando Piopitas...
echo ============================================

python -m venv venv
call venv\Scripts\activate.bat

pip install -r requirements.txt

python manage.py makemigrations app_piopitas
python manage.py migrate
python manage.py poblar_menu
python manage.py crear_admin_demo

echo ============================================
echo   Listo. Abre http://127.0.0.1:8000 en tu navegador
echo   Panel admin: http://127.0.0.1:8000/inicioSA
echo   Correo: admin@piopitas.com
echo   Contraseña: Piopitas123
echo ============================================

python manage.py runserver
