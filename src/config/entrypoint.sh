# python manage.py runserver

APP_PORT = ${PORT:-8000}

cd /app/
/opt/venv/bin/gunicore core.wsgi:application --bind "0.0.0.0:${APP_PORT}"