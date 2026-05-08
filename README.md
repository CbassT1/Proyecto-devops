# Proyecto Final - Fundamentos de DevOps

**Autores:** 
* Sebastian Daniel Mata Trevino
* Yamil Alejandro Ramirez Perez

---

## Descripcion del Proyecto
Este repositorio contiene la infraestructura como codigo (IaC), los scripts de automatizacion y las configuraciones de despliegue continuo para Soluciones Tecnologicas del Futuro. La aplicacion esta basada en Flask y Nginx, empaquetada con Docker y desplegada en AWS (Learner Lab).

El objetivo es transicionar de un modelo de entrega manual a una plataforma totalmente automatizada (CI/CD, Monitoreo y Seguridad), optimizando los tiempos de entrega y mejorando la estabilidad de las aplicaciones.

---

## Arquitectura del Sistema
El sistema sigue una arquitectura de microservicios contenedorizados y aprovisionamiento IaC:

1. Infraestructura como Codigo (IaC): La VPC, Subredes Publicas y Privadas, Security Groups restrictivos, bucket S3 y EC2 se aprovisionan via AWS CloudFormation.
2. Proxy Inverso y Backend: Contenedor Nginx (puerto 8080) que enruta trafico hacia un contenedor Flask (puerto 5000) a traves de una red Bridge local (stf_network).
3. Microservicio Serverless: Una funcion independiente alojada en AWS Lambda (con concurrencia restringida a 10) detras de un API Gateway.
4. Monitoreo y Auditoria: Integracion con el agente de CloudWatch (logs del sistema operativo y alarmas de CPU) y AWS Config para la trazabilidad de los recursos.

---

## Estructura del Repositorio

* app-docker/
    * app.py / test_app.py: Codigo backend y pruebas unitarias con Pytest.
    * Dockerfile: Imagen Multi-stage build para reducir peso y superficie de ataque.
    * docker-compose.yaml: Orquestador de la red de contenedores.
    * nginx.conf: Archivo de configuracion del proxy inverso.
    * requirements.txt: Dependencias de Python.
* .github/workflows/
    * pipeline.yml: Flujo de integracion y entrega continua automatizado.
* automatizacion.py / aws_boto3_avanzado.py: Scripts de Boto3 para aprovisionamiento de EC2, AutoScaling, gestion de S3 y bases de datos DynamoDB.
* infraestructura.yaml: Plantilla YAML de AWS CloudFormation para despliegue de red y computo.
* rollback.sh: Script de contingencia para restaurar la aplicacion ante fallos en produccion.
* setup.sh: Script para inicializar y configurar el entorno de la instancia EC2.

---

## Pipeline CI/CD y Justificaciones Arquitectonicas (Learner Lab)

Debido a las estrictas politicas de Service Control Policies (SCPs) y Permission Boundaries del entorno AWS Learner Lab, se realizaron las siguientes adaptaciones estrategicas DevOps:

1. GitHub Actions vs CodePipeline / SSM:
   Las restricciones del rol LabRole impiden la configuracion completa de agentes de AWS Systems Manager (SSM) para despliegues automatizados y la creacion de Service-Linked Roles para CodePipeline. Por ello, se implemento un pipeline en GitHub Actions inyectando llaves seguras (ssh-action) como alternativa profesional.

2. Pruebas Automatizadas y Smart Wait:
   Tras la ejecucion de docker-compose, el pipeline lanza un script de sondeo HTTP local que valida la respuesta de la aplicacion. Exige un codigo 200 OK antes de marcar el despliegue como exitoso.

3. Mecanismo de Rollback (Bash vs Lambda):
   La arquitectura ideal exigia el uso de AWS Lambda para automatizar el rollback ante fallos. Sin embargo, conectar una funcion Lambda a una instancia EC2 dentro de una VPC privada requiere permisos IAM especificos (ec2:CreateNetworkInterface) que el Learner Lab deniega explicitamente. Se implemento un mecanismo de autorecuperacion nativo en Bash (rollback.sh) que revierte al ultimo commit funcional y reinicia los contenedores.
