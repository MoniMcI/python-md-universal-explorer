# 📊 Lector Universal de Documentación Markdown - Tienda Aurelion

## 🎯 Descripción

Este proyecto es un **lector universal de documentos Markdown** pensado inicialmente para leer la documentación de la Tienda Aurelion (documentacion.md).
Permite navegar interactivamente por secciones de cualquier archivo `.md` y consultar contenido de forma cómoda.

Inicialmente se realizó una versión simple **CLI** que analiza solamente el documento de la Tienda Aurelión. Posteriormente se implementó una mejora para que acepte cualquier documento Markdown que el usuario suba, mostrando las secciones principales del mismo. Esta mejora se implementó en las versiones **GUI** y **Streamlit**

Los programas son:

1- Version CLI: consulta_documentacion.py  
2- Version GUI: md_explorer_gui.py  
3- Version Web: universal_md_explorer.py

## 💻 Versión CLI

Esta versión del programa python (**consulta_documentacion.py**) es la más simple y no necesita ninguna librería para funcionar. Simplemente se debe descargar todo el proyecto y ejecutar el programa como se indica a continuación:

**Interfaz de Línea de Comandos (CLI)**

    ```bash
    python consulta_documentacion.py
    ```

**Características:**

- Explora documentacion.md por secciones.

- Busca palabras clave.

- Verifica el sistema automáticamente.

## 🖥️ Versión GUI (Interfaz Gráfica)

Una interfaz gráfica moderna desarrollada con **CustomTkinter** que proporciona una experiencia visual mejorada para explorar la documentación.

**Instalación y ejecución:**

```bash
pip install customtkinter pillow
python md_explorer_gui.py
```

**Características:**

- **Interfaz moderna**: Diseño contemporáneo con soporte para temas claro y oscuro.

- **Soporte para imágenes**: Visualización de diagramas PNG inline (requiere Pillow).

- **Navegación lateral**: Panel scrolleable con todas las secciones de la documentación.

- **Visualización mejorada**: Área principal con texto formateado y scroll automático.

- **Cambio de tema**: Botón para alternar entre modo claro y oscuro.

- **Detección automática**: Carga automáticamente `docs/documentacion.md`.

- **Fácil navegación**: Un clic en cualquier sección la muestra en el panel principal.

## 🌐 Version Web usando Streamlit

La versión web utiliza **Streamlit** para crear una aplicación interactiva que se ejecuta en el navegador. Esta implementación convierte automáticamente el archivo Markdown en una interfaz web navegable con menús laterales dinámicos, búsqueda en tiempo real y visualización optimizada para documentos largos.

Ejecuta la app web localmente:

```bash
pip install streamlit
streamlit run universal_md_explorer.py
```

**Características:**

- Navegación lateral automática por secciones detectadas.

- Búsqueda por texto en todo el documento.

- Vista paginada para secciones largas.

- Subir nuevos archivos Markdown a `docs/` o cargar desde la app.

⚠️ Nota: Los datos CSV están previstos para futuras etapas de análisis y no se requieren para esta app de visualización de Markdown.

Puedes probar la aplicacion web directamente en este enlace:

🌐 **[Ver Aplicación Web en vivo](https://python-md-universal-explorer.streamlit.app/)**

## 📁 Estructura del Proyecto

```text
proyecto/
├── data/                      # CSVs para futura etapa de análisis
├── docs/                      # Documentación del proyecto
│   ├── documentacion.md       # Documentación principal
│   └── instrucciones_copilot.md
├── images/                    # Imágenes y diagramas
│   └── diagrama-flujo.png     # Diagrama de flujo del programa
├── utils/                     # Funciones auxiliares
│   └── utils.py               # Utilidades para parsing Markdown
├── consulta_documentacion.py  # Script CLI
├── md_explorer_gui.py         # Interfaz Gráfica - CustomTkinter
├── universal_md_explorer.py   # App Web - Streamlit
├── README.md                  # Este archivo
└── requirements.txt           # Dependencias del proyecto
```

## 📦 Dependencias

1- Versión CLI: Solo la biblioteca estándar de Python es necesaria para CLI.

2- Versión GUI: Para el explorador con interfaz gráfica:

```bash
pip install customtkinter pillow
```

3- Version Web con Streamlit:

```bash
pip install streamlit
```

## 📞 Contacto

**Desarrollador:** Mónica Guantay  
**Email:** [mbguantay@gmail.com](mailto:mbguantay@gmail.com)  
**Proyecto:** Análisis de Datos con IA - Tienda Aurelion - Curso Guayerd
