#!/usr/bin/env bash

set -euo pipefail

CONTAINER_NAME="oracle-free"
IMAGE="gvenzl/oracle-free:latest"
PASSWORD="YourStrongPass1"
PORT=1521

echo "=== Starting Oracle Free container ==="

# Remove existing container if present
if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}\$"; then
  echo "Container ${CONTAINER_NAME} exists. Removing..."
  docker rm -f "${CONTAINER_NAME}"
fi

echo "Pulling latest image..."
docker pull "${IMAGE}"

echo "Running container..."
docker run -d \
  --name "${CONTAINER_NAME}" \
  -p ${PORT}:1521 \
  -e ORACLE_PASSWORD="${PASSWORD}" \
  "${IMAGE}"

echo "Waiting for database to become ready..."

# Wait for readiness message
until docker logs "${CONTAINER_NAME}" 2>&1 | grep -q "DATABASE IS READY"; do
  sleep 3
  echo "Still waiting..."
done

echo ""
echo "=== Oracle is ready ==="
echo "Host: 127.0.0.1"
echo "Port: ${PORT}"
echo "Service: FREEPDB1"
echo "User: system"
echo ""
echo "Export these variables before running profiler:"
echo ""
echo "export DB_USER=system"
echo "export DB_PASSWORD='${PASSWORD}'"
echo "export DB_HOST=127.0.0.1"
echo "export DB_PORT=${PORT}"
echo "export DB_SERVICE=FREEPDB1"
echo ""
