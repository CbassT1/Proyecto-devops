#!/bin/bash

# Actualizar la lista de paquetes
echo "Actualizando el sistema..."
sudo apt-get update -y

# Instalar Git, Vim y Python3
echo "Instalando dependencias básicas (Git, Vim, Python3)..."
sudo apt-get install -y git vim python3 python3-pip

# Instalar Docker
echo "Instalando Docker..."
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Crear script para limpieza de logs
echo "Configurando limpieza automática de logs..."
echo '#!/bin/bash' > /home/ubuntu/clean_logs.sh
echo 'sudo journalctl --vacuum-time=7d' >> /home/ubuntu/clean_logs.sh
chmod +x /home/ubuntu/clean_logs.sh

# Programar la tarea con cron (se ejecuta todos los domingos a las 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * 0 /home/ubuntu/clean_logs.sh") | crontab -

echo "¡Instalación y configuración completada con éxito!"