# Querypunk

Querypunk es un videojuego narrativo por niveles centrado en la enseñanza y aprendizaje del lenguaje SQL.

## Estructura

- `frontend/`: cliente React + TypeScript
- `backend/`: servidor FastAPI + bases de datos
- `docs/`: documentación del TFG

## Requisitos

Para ejecutar Querypunk es necesario disponer de:

- Docker Desktop
- Docker Compose
- Git
- Ollama
- Modelo `llama3` de Ollama
- Navegador web actualizado

## Instalación de Ollama

Querypunk utiliza Ollama para generar mediante inteligencia artificial determinados elementos narrativos de los retos.

Ollama debe instalarse directamente en el equipo donde se ejecuta Querypunk. No se ejecuta dentro de un contenedor Docker.

Una vez instalado Ollama, descargar el modelo utilizado por la aplicación:

```bash
ollama pull llama3
