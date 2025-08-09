#!/usr/bin/env bash
set -e

# Default to Postgres; allow SQLite fallback if USE_SQLITE=1
if [ "${USE_SQLITE}" != "1" ]; then
  echo "Waiting for Postgres at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
  python - <<'PY'
import os, time, sys
import psycopg2
host=os.getenv('POSTGRES_HOST','db')
port=int(os.getenv('POSTGRES_PORT','5432'))
user=os.getenv('POSTGRES_USER','jobboard')
password=os.getenv('POSTGRES_PASSWORD','jobboard')
dbname=os.getenv('POSTGRES_DB','jobboard')
for i in range(60):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
        conn.close()
        print('Postgres is ready')
        sys.exit(0)
    except Exception as e:
        time.sleep(1)
print('Postgres not available after waiting', file=sys.stderr)
sys.exit(1)
PY
fi

python manage.py migrate --noinput
# Optional in case you serve static files elsewhere
python manage.py collectstatic --noinput || true

# Start server
if [ "${DJANGO_DEBUG}" = "1" ]; then
  echo "Starting Django development server..."
  exec python manage.py runserver 0.0.0.0:8000
else
  echo "Starting Gunicorn..."
  exec gunicorn jobboard.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi 