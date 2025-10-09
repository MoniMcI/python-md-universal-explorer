#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explorador Universal de Documentos Markdown - Tienda Aurelion

Aplicación web con Streamlit que permite visualizar cualquier documento Markdown
de forma interactiva, con detección automática de estructura y navegación lateral.
Adaptado para la nueva estructura de proyecto con carpetas organizadas.

Uso:
    streamlit run src/universal_md_explorer.py
"""

import streamlit as st
import os
import sys

# Añadir el directorio src al path para importar utils
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(current_dir)

from utils import (
    get_project_paths,
    load_markdown,
    parse_markdown_sections,
    discover_markdown_files,
    discover_csv_files,
    get_file_info,
    clean_markdown_content,
    get_markdown_stats
)


def setup_page_config():
    """Configura la página de Streamlit con tema y layout."""
    st.set_page_config(
        page_title="Universal Markdown Doc Explorer",
        page_icon="📘",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_custom_styles():
    """Aplica estilos CSS personalizados para mejorar la apariencia."""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #2E8B57 0%, #228B22 100%);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 1rem;
        }
        
        .doc-info-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .section-content {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #2E8B57;
        }
        
        .csv-info {
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 6px;
        }
        
        .stMarkdown img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .stMarkdown table {
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }
        
        .stMarkdown th, .stMarkdown td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        .stMarkdown th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)


def render_main_header(title: str):
    """Renderiza el header principal de la aplicación."""
    st.markdown(f"""
    <div class="main-header">
        <h1>Universal Markdown Doc Explorer</h1>
        <p>Explorador universal de documentos Markdown (md)</p>
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)


# def render_project_structure():
#     """Muestra la estructura del proyecto en la sidebar."""
#     st.sidebar.markdown("### 📁 Estructura del Proyecto")
#     
#     base_dir, data_dir, docs_dir, src_dir = get_project_paths()
#     
#     # Verificar qué carpetas existen
#     structure_info = []
#     
#     if os.path.exists(data_dir):
#         csv_files = discover_csv_files(data_dir)
#         structure_info.append(f"📊 **data/** ({len(csv_files)} archivos CSV)")
#     
#     if os.path.exists(docs_dir):
#         md_files = discover_markdown_files(docs_dir)
#         structure_info.append(f"📄 **docs/** ({len(md_files)} archivos MD)")
#     
#     if os.path.exists(src_dir):
#         py_files = [f for f in os.listdir(src_dir) if f.endswith('.py')]
#         structure_info.append(f"🐍 **src/** ({len(py_files)} archivos Python)")
#     
#     for info in structure_info:
#         st.sidebar.markdown(info)


def display_csv_explorer():
    """Muestra el explorador de archivos CSV."""
    st.markdown("## 📊 Explorador de Datos CSV")
    
    _, data_dir, _, _ = get_project_paths()
    csv_files = discover_csv_files(data_dir)
    
    if not csv_files:
        st.warning("📭 No se encontraron archivos CSV en la carpeta `data/`")
        return
    
    # Selector de archivo CSV
    csv_names = [os.path.basename(f) for f in csv_files]
    selected_csv = st.selectbox("Seleccionar archivo CSV:", csv_names)
    
    if selected_csv:
        selected_path = None
        for path in csv_files:
            if os.path.basename(path) == selected_csv:
                selected_path = path
                break
        
        if selected_path:
            file_info = get_file_info(selected_path)
            
            st.markdown(f"""
            <div class="csv-info">
                <h4>📄 {file_info['name']}</h4>
                <p><strong>Tamaño:</strong> {file_info['size']}</p>
                <p><strong>Ubicación:</strong> <code>data/{selected_csv}</code></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar primeras líneas del CSV
            try:
                import pandas as pd
                df = pd.read_csv(selected_path, nrows=10)
                
                st.markdown("**Vista previa (primeras 10 filas):**")
                st.dataframe(df, width='stretch')
                
                st.markdown("**Información del dataset:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📋 Columnas", len(df.columns))
                with col2:
                    st.metric("📊 Filas (muestra)", len(df))
                with col3:
                    st.metric("🔢 Tipos únicos", df.dtypes.nunique())
                
                # Mostrar esquema
                with st.expander("🔍 Ver esquema completo"):
                    schema_data = []
                    for col in df.columns:
                        schema_data.append({
                            'Columna': col,
                            'Tipo': str(df[col].dtype),
                            'Valores únicos': df[col].nunique(),
                            'Nulos': df[col].isnull().sum()
                        })
                    
                    schema_df = pd.DataFrame(schema_data)
                    st.dataframe(schema_df, width='stretch')
                    
            except ImportError:
                st.info("💡 Instala pandas para ver vista previa: `pip install pandas`")
            except Exception as e:
                st.error(f"❌ Error al leer CSV: {str(e)}")


def on_section_change():
    """Callback para cuando cambia la sección seleccionada."""
    if 'section_radio' in st.session_state:
        st.session_state.current_section = st.session_state.section_radio


def main():
    """Función principal de la aplicación."""
    setup_page_config()
    apply_custom_styles()
    
    # Inicializar variables de estado de forma más robusta
    if 'current_section' not in st.session_state:
        st.session_state.current_section = None
    if 'current_document' not in st.session_state:
        st.session_state.current_document = None
    
    # Obtener rutas del proyecto
    base_dir, data_dir, docs_dir, src_dir = get_project_paths()
    
    # Descubrir archivos Markdown en docs/
    markdown_files = discover_markdown_files(docs_dir)
    
    # Sidebar: Selección de documento (compacto como en GUI)
    st.sidebar.markdown("---")
    st.sidebar.markdown("## � Documentos")
    
    # Sección compacta: dropdown + upload en el mismo bloque
    with st.sidebar.container():
        if markdown_files:
            # Crear opciones amigables (solo nombres de archivo)
            file_options = ["Seleccionar documento..."] + [
                os.path.basename(file) for file in markdown_files
            ]
            
            selected_file_name = st.selectbox(
                "📚 Docs disponibles:",
                file_options,
                key="file_selector"
            )
            
            # Encontrar la ruta completa del archivo seleccionado
            selected_file_path = None
            if selected_file_name != "Seleccionar documento...":
                for file_path in markdown_files:
                    if os.path.basename(file_path) == selected_file_name:
                        selected_file_path = file_path
                        break
        else:
            st.warning("📭 No se encontraron archivos .md en `docs/`")
            selected_file_path = None
        
        # Upload en la misma sección (compacto)
        uploaded_file = st.file_uploader(
            "📂 O cargar otro archivo:",
            type=['md', 'markdown'],
            help="Archivo temporal",
            key="file_uploader"
        )
    
    # Determinar qué contenido mostrar
    document_content = ""
    document_title = "Explorador de Documentos"
    is_uploaded = False
    
    if uploaded_file is not None:
        # Prioridad al archivo subido
        try:
            document_content = uploaded_file.read().decode('utf-8')
            document_title = f"📤 {uploaded_file.name}"
            is_uploaded = True
            st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"❌ Error al cargar: {str(e)}")
    elif selected_file_path:
        # Archivo local seleccionado
        document_content = load_markdown(selected_file_path)
        if not document_content:
            st.sidebar.error("❌ No se pudo cargar el archivo seleccionado")
        else:
            # Resetear sección si cambió el documento
            if st.session_state.current_document != selected_file_path:
                st.session_state.current_document = selected_file_path
                st.session_state.current_section = None
    
    # Procesar contenido si existe
    if document_content:
        title, sections = parse_markdown_sections(document_content)
        
        if title:
            document_title = title
        
        # Calcular estadísticas
        stats = get_markdown_stats(document_content)
        
        # Renderizar header principal
        render_main_header(document_title)
        
        # Mostrar información del documento
        if not is_uploaded and selected_file_path:
            file_info = get_file_info(selected_file_path)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Palabras", stats['words'])
            with col2:
                st.metric("📋 Líneas", stats['lines'])
            with col3:
                st.metric("🔖 Secciones", stats['sections'])
            with col4:
                st.metric("💾 Tamaño", file_info['size'])
        
        # Navegación por pestañas
        tab1, tab2 = st.tabs(["📖 Contenido del Documento", "📊 Explorar Datos CSV"])
        
        with tab1:
            if sections:
                # Navegación lateral por secciones (inmediatamente después de selección de archivo)
                st.sidebar.markdown("---")
                st.sidebar.markdown("## 🧭 Navegación")
                
                section_options = list(sections.keys())
                
                # Inicializar sección por defecto si es necesario
                if 'current_section' not in st.session_state or st.session_state.current_section not in section_options:
                    st.session_state.current_section = section_options[0]
                
                # Radio button con callback - esto soluciona el problema del doble clic
                current_index = section_options.index(st.session_state.current_section)
                
                st.sidebar.radio(
                    "📄 Secciones:",
                    section_options,
                    index=current_index,
                    key="section_radio",
                    on_change=on_section_change
                )
                
                # Usar la sección actual del estado
                selected_section = st.session_state.current_section
                
                # Mostrar contenido de la sección
                if selected_section in sections:
                    section_content = sections[selected_section]
                    
                    st.markdown(f"""
                    <div class="section-content">
                        <h2>📖 {selected_section}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Renderizar contenido
                    clean_content = clean_markdown_content(section_content)
                    if clean_content.strip():
                        st.markdown(clean_content, unsafe_allow_html=True)
                    else:
                        st.info("Esta sección está vacía.")
            else:
                # Sin secciones definidas
                st.warning("⚠️ Este documento no tiene secciones definidas (##). Mostrando contenido completo:")
                clean_content = clean_markdown_content(document_content)
                st.markdown(clean_content, unsafe_allow_html=True)
        
        with tab2:
            display_csv_explorer()
    
    else:
        # No hay contenido - mostrar página de bienvenida
        render_main_header("Bienvenido al Explorador")
        
        st.markdown("""
        ## 🏠 Bienvenido al Universal Markdown Doc Explorer
        
        ### 📁 Estructura del Proyecto
        Este explorador está diseñado para trabajar con la siguiente estructura:
        
        ```
        proyecto/
        ├── data/                    # Archivos CSV de datos
        ├── docs/                    # Documentación en Markdown  
        ├── src/                     # Código fuente Python
        ├── consulta_documentacion.py
        └── README.md
        ```
        
        ### 🚀 Cómo usar
        
        1. **📄 Explorar documentación**: Selecciona un archivo .md de la carpeta `docs/`
        2. **📊 Explorar datos**: Ve a la pestaña "Explorar Datos CSV" para ver archivos en `data/`
        3. **📤 Subir temporal**: Usa el uploader para ver cualquier archivo Markdown
        
        ### ✨ Características
        - 🔍 Detección automática de título y secciones
        - 🧭 Navegación lateral inteligente
        - 📊 Vista previa de datos CSV con pandas
        - 📱 Diseño responsive
        - 🎨 Interfaz moderna y limpia
        """)
        
        # Mostrar estado actual de carpetas
        st.markdown("### 📊 Estado Actual del Proyecto")
        
        _, data_dir, docs_dir, src_dir = get_project_paths()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_count = len(discover_csv_files(data_dir)) if os.path.exists(data_dir) else 0
            st.metric("📊 Archivos CSV", csv_count, help=f"En carpeta data/")
        
        with col2:
            md_count = len(discover_markdown_files(docs_dir)) if os.path.exists(docs_dir) else 0
            st.metric("📄 Archivos MD", md_count, help=f"En carpeta docs/")
        
        with col3:
            py_count = len([f for f in os.listdir(src_dir) if f.endswith('.py')]) if os.path.exists(src_dir) else 0
            st.metric("🐍 Archivos Python", py_count, help=f"En carpeta src/")


if __name__ == "__main__":
    main()