#!/bin/bash
echo "Fallo detectado. Iniciando proceso de Rollback..."
cd /home/ubuntu/Proyecto-devops

# 1. Regresar el repositorio al commit anterior (la última versión estable)
git reset --hard HEAD~1

# 2. Reconstruir los contenedores con la versión estable
cd app-docker
sudo docker-compose down
sudo docker-compose up -d --build

echo "Rollback completado. Sistema restaurado."