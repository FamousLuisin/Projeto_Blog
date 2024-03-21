# shebang: tentar executar esse arquivo como /bin/sh
#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..." &
  sleep 0.1
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Esses comandos tão sendo executados pq no Dockerfile ja nos colocou na pasta do projeto django
python manage.py collectstatic
python manage.py migrate
python manage.py runserver