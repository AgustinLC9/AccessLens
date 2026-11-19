# AccessLens

**Análisis automatizado de accesibilidad web mediante inteligencia artificial.**

AccessLens es una aplicación de escritorio desarrollada en Python que permite analizar sitios web para identificar posibles problemas de accesibilidad, evaluar sus resultados y ofrecer recomendaciones para mejorar la experiencia de los usuarios.

El proyecto combina automatización de navegadores, análisis de accesibilidad e inteligencia artificial local.

## Características principales

- **Análisis de múltiples páginas:** permite analizar varias URL en una misma ejecución.
- **Detección de problemas:** utiliza Playwright y axe-core para identificar problemas de accesibilidad.
- **Procesamiento concurrente:** analiza páginas en paralelo para optimizar los tiempos de ejecución.
- **Cancelación de análisis:** permite interrumpir los procesos en curso de forma controlada.
- **Inteligencia artificial local:** utiliza Ollama para generar explicaciones y recomendaciones sobre los problemas detectados.
- **Informes individuales y generales:** presenta los resultados de cada página y un resumen del análisis completo.
- **Historial de análisis:** almacena los resultados para poder consultarlos posteriormente.
- **Persistencia de datos:** utiliza SQLite para guardar la información.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| PySide6 | Interfaz gráfica |
| Playwright | Automatización del navegador |
| axe-core | Detección de problemas de accesibilidad |
| Ollama | Ejecución local del modelo de IA |
| Qwen 2.5 3B | Generación de explicaciones y recomendaciones |
| SQLite | Persistencia de datos |
| ThreadPoolExecutor | Procesamiento concurrente |

## Estructura del proyecto

```text
AccessLens/
├── analisis/       # Lógica de análisis de páginas
├── bdd/            # Conexión y acceso a la base de datos
├── ia/             # Integración con inteligencia artificial
├── interfaz/       # Componentes de la interfaz gráfica
├── recursos/       # Recursos y archivos auxiliares
├── main.py         # Punto de entrada de la aplicación
└── requirements.txt
```

## Requisitos

- Python instalado.
- Ollama instalado y en ejecución para utilizar las recomendaciones mediante IA.
- Modelo `qwen2.5:3b` descargado en Ollama.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/AgustinLC9/AccessLens.git
cd AccessLens
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activarlo en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Chromium para Playwright

```bash
python -m playwright install chromium
```

### 5. Configurar Ollama

Descargar el modelo:

```bash
ollama pull qwen2.5:3b
```

Asegurarse de que Ollama esté ejecutándose antes de utilizar las funciones de inteligencia artificial.

### 6. Ejecutar AccessLens

```bash
python main.py
```

## Procesamiento concurrente

AccessLens incorpora procesamiento concurrente mediante `ThreadPoolExecutor`, permitiendo analizar varias páginas simultáneamente.

También implementa mecanismos de cancelación cooperativa mediante `threading.Event`, para gestionar la interrupción de los análisis sin dejar procesos innecesariamente activos.

## Inteligencia artificial

La aplicación utiliza Ollama para ejecutar un modelo de lenguaje local. La IA complementa los resultados del análisis automatizado mediante explicaciones y recomendaciones orientadas a facilitar la comprensión de los problemas encontrados.

## Alcance

AccessLens es un proyecto académico y experimental. Los análisis automatizados no garantizan el cumplimiento completo de las pautas WCAG ni reemplazan una evaluación manual de accesibilidad.

---

**Desarrollado como proyecto final de Programación Avanzada.**