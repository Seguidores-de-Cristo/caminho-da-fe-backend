#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "1) Verificando e liberando porta 8000..."
pids=$(lsof -ti:8000 || true)
if [ -n "$pids" ]; then
  echo "Matando PIDs: $pids"
  kill -9 $pids || true
  sleep 1
else
  echo "Porta 8000 livre"
fi

echo "2) Subindo serviços Docker (se aplicável)..."
if [ -f docker-compose.yaml ]; then
  docker compose up -d
fi

echo "3) Aguardando banco de dados na porta 3306 (até 60s)..."
timeout=60
count=0
while ! bash -c "</dev/tcp/127.0.0.1/3306" >/dev/null 2>&1; do
  sleep 1
  count=$((count+1))
  if [ $count -ge $timeout ]; then
    echo "Timeout esperando DB. Continue mesmo assim? (y/N)"
    read -r ans
    if [ "$ans" != "y" ]; then
      echo "Abortando devido a DB indisponível"
      exit 1
    else
      break
    fi
  fi
done

echo "4) Aplicando migrations (alembic upgrade head)..."
poetry run alembic upgrade head

echo "5) Iniciando uvicorn na porta 8000 (em background)..."
mkdir -p logs
nohup poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/uvicorn.log 2>&1 &
echo $! > .uvicorn.pid
echo "uvicorn iniciado (PID $(cat .uvicorn.pid)). Logs em logs/uvicorn.log"

exit 0
