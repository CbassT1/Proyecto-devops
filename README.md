# Proyecto Final - Fundamentos de DevOps

**Autores:** 
* Sebastián Daniel Mata Treviño
* Yamil Alejandro Ramírez Pérez

---

## Descripción del Proyecto
Este repositorio contiene la infraestructura como código (IaC), los scripts de automatización y las configuraciones de despliegue continuo para una aplicación web basada en **Flask** y **Nginx**. El proyecto fue diseñado para ejecutarse en un entorno contenedorizado utilizando **Docker** y desplegado en la nube a través de **AWS Learner Lab**.

El objetivo principal es demostrar la aplicación práctica de los principios de DevOps mediante la automatización del aprovisionamiento, la configuración y el despliegue continuo (CI/CD).

---

## Arquitectura del Sistema
El sistema sigue una arquitectura de microservicios contenedorizados:

1.  **Backend (Aplicación):** Desarrollado en Python con el framework **Flask**.
2.  **Servidor Web / Proxy Inverso:** Se utiliza **Nginx** para gestionar las peticiones HTTP y redirigirlas a la aplicación Flask.
3.  **Orquestación Local:** Los servicios se construyen y levantan utilizando **Docker Compose**.
4.  **Hosting:** La aplicación reside en una instancia **Amazon EC2 (t2.micro)** aprovisionada en AWS.
5.  **CI/CD:** El despliegue está completamente automatizado utilizando **GitHub Actions**.

---

## Estructura del Repositorio

* 📁 `app-docker/`
    * `app.py`: Código fuente de la aplicación Flask.
    * `requirements.txt`: Dependencias de Python.
    * `Dockerfile`: Configuración de la imagen de la aplicación utilizando un enfoque *Multi-stage build* para optimizar el peso final.
    * `nginx.conf`: Archivo de configuración del proxy inverso.
    * `docker-compose.yml`: Orquestador de los contenedores para levantar Nginx y Flask en una red compartida (`stf_network`).
* 📁 `.github/workflows/`
    * `pipeline.yml`: Flujo de trabajo de GitHub Actions para Integración y Entrega Continua.
* 📄 `automatizacion.py`: Script en Python utilizando la librería **Boto3** para la gestión y consulta de recursos en AWS.
* 📄 `setup.sh`: Script en Bash para la preparación inicial del entorno (instalación de Docker, Docker Compose y Git) en el servidor Linux.
* 📄 `infraestructura.yaml`: Plantilla de **AWS CloudFormation** para la creación y aprovisionamiento de la red y la instancia EC2.
* 📄 `rollback.sh`: Script de seguridad en Bash diseñado para regresar al commit estable anterior y reiniciar los servicios en caso de un fallo en el despliegue.

---

## Flujo de CI/CD (Pipeline)

> **Nota Técnica:** Durante la fase de desarrollo, se detectó que el entorno educativo *AWS Learner Lab* restringe los permisos IAM (`AccessDeniedException`) necesarios para CodeBuild y CodePipeline. Con previa autorización, se diseñó e implementó este pipeline utilizando **GitHub Actions** como alternativa profesional.

Cada vez que se realiza un *Push* o *Merge* a las ramas principales (`develop` o `main`), GitHub Actions ejecuta el siguiente flujo:

1.  **Conexión Segura:** Se conecta vía SSH a la instancia EC2 de producción utilizando secretos del repositorio (Llaves PEM y Token de acceso).
2.  **Sincronización:** Forzado de actualización del código fuente (`git fetch` y `git reset --hard`).
3.  **Construcción y Despliegue:** Reconstrucción de los contenedores eliminando huérfanos (`docker-compose down/up --build --remove-orphans`).
4.  **Validación Continua (Smart Wait):** Ejecución de múltiples peticiones automatizadas (cada 5 segundos) al puerto local para validar la respuesta HTTP.
5.  **Rollback Automático:** Si la aplicación no devuelve un código de estado `200 OK` tras varios intentos, el pipeline se marca como fallido y ejecuta automáticamente el script `rollback.sh` para restaurar la última versión funcional y garantizar la alta disponibilidad.
