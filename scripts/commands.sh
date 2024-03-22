#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

wait_psql.sh

# Esses comandos tão sendo executados pq no Dockerfile ja nos colocou na pasta do projeto django
collectstatic.sh
migrate.sh
runserver.sh