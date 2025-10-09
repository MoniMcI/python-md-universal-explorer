# 📊 Lector Universal de Documentación Markdown - Tienda Aurelion

## 🎯 Descripción

Este proyecto es un **lector universal de documentos Markdown** pensado inicialmente para la documentación de la Tienda Aurelion.  
Permite navegar interactivamente por secciones de cualquier archivo `.md` y consultar contenido de forma cómoda en **CLI, Notebook o navegador** (Streamlit).

## 🌐 Demo Web (Streamlit)

Ejecuta la app web localmente:

```bash
pip install streamlit
streamlit run src/universal_md_explorer.py
```

**Características:**

- Navegación lateral automática por secciones detectadas.

- Búsqueda por texto en todo el documento.

- Vista paginada para secciones largas.

- Permite seleccionar y cargar múltiples Markdown.

⚠️ Nota: Los datos CSV están previstos para futuras etapas de análisis y no se requieren para esta app de visualización de Markdown.

## 💻 Uso Local

  1. Interfaz de Línea de Comandos (CLI)

      ```bash
      python consulta_documentacion.py
      python consulta_documentacion.py --autotest
      ```

      - Explora documentacion.md por secciones.

      - Busca palabras clave.

      - Verifica el sistema automáticamente.

## 📁 Estructura del Proyecto

```text
proyecto/
├── data/                      # CSVs para futura etapa de análisis
├── docs/                      # Documentación original en Markdown
│   ├── documentacion.md
│   └── instrucciones_copilot.md
├── src/                       # Código fuente
│   ├── utils.py               # Funciones auxiliares
│   └── universal_md_explorer.py  # App Streamlit
├── consulta_documentacion.py  # Script CLI
├── md_explorer_gui.py         # Interfaz Gráfica - Customtkinter
├── README.md                  # Este archivo
└── requirements.txt           # Este archivo
```

## 🧩 Funcionalidades Principales

- **Carga automática** de Markdown.

- **Detección inteligente** de secciones por encabezados (##).

- **Menú lateral** en Streamlit para navegación.

- **Selección múltiple de documentos.**

- **Paginación** para secciones largas.

- **Renderizado seguro de HTML** para mejorar legibilidad.

## 📦 Dependencias

Solo la biblioteca estándar de Python es necesaria para CLI.
Para Streamlit:

```bash
pip install streamlit
```

Para el explorador con interfaz gráfica:

```bash
pip install customtkinter
```

## 🚀 Cómo Contribuir / Extender

- Subir nuevos archivos Markdown a docs/ o cargar desde la app.

- Mejorar la interfaz Streamlit (temas, filtros, búsqueda avanzada).

- Integrar análisis de CSV para futuros reportes y visualizaciones.

## 📞 Contacto

**Desarrollador:** Mónica Guantay  
**Email:** [mbguantay@gmail.com](mailto:mbguantay@gmail.com)  
**Proyecto:** Análisis de Datos con IA - Tienda Aurelion
