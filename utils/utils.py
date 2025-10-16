#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para el explorador de documentos Markdown - Tienda Aurelion

Este módulo contiene funciones reutilizables para parsear y cargar
documentos Markdown de forma robusta, con manejo de errores y
detección automática de estructura.
"""

import os
import re
from typing import Dict, Tuple, List, Optional


def get_project_paths():
    """
    Obtiene las rutas base del proyecto según la nueva estructura.
    
    Returns:
        tuple: (base_dir, data_dir, docs_dir, utils_dir)
    """
    # Obtener directorio base del proyecto (donde están los scripts principales)
    current_file = os.path.abspath(__file__)     # utils/utils.py
    utils_dir = os.path.dirname(current_file)    # utils/
    base_dir = os.path.dirname(utils_dir)        # proyecto/
    
    data_dir = os.path.join(base_dir, 'data')
    docs_dir = os.path.join(base_dir, 'docs')
    
    return base_dir, data_dir, docs_dir, utils_dir


def load_markdown(path: str) -> str:
    """
    Carga un archivo Markdown desde disco con manejo robusto de encoding.
    
    Args:
        path (str): Ruta al archivo Markdown
        
    Returns:
        str: Contenido del archivo, o string vacío si hay error
    """
    if not os.path.exists(path):
        return ""
    
    if not os.path.isfile(path):
        return ""
    
    # Intentar diferentes encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            continue
        except (IOError, OSError, PermissionError):
            return ""
    
    return ""


def parse_markdown_sections(content: str) -> Tuple[str, Dict[str, str]]:
    """
    Parsea un documento Markdown y extrae título principal y secciones.
    
    Args:
        content (str): Contenido completo del documento Markdown
        
    Returns:
        Tuple[str, Dict[str, str]]: (titulo_principal, {nombre_seccion: contenido})
    """
    if not content.strip():
        return "", {}
    
    lines = content.split('\n')
    
    # Buscar título principal (primer #)
    main_title = ""
    title_pattern = re.compile(r'^#\s+(.+)$')
    
    for line in lines:
        match = title_pattern.match(line.strip())
        if match:
            main_title = match.group(1).strip()
            break
    
    if not main_title:
        main_title = "Documento"
    
    # Parsear secciones (##)
    sections = {}
    current_section = None
    current_content = []
    section_pattern = re.compile(r'^##\s+(.+)$')
    
    for line in lines:
        section_match = section_pattern.match(line.strip())
        
        if section_match:
            # Guardar sección anterior si existe
            if current_section is not None:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Iniciar nueva sección
            current_section = section_match.group(1).strip()
            current_content = []
        else:
            # Añadir línea al contenido de la sección actual
            if current_section is not None:
                current_content.append(line)
    
    # Guardar última sección
    if current_section is not None:
        sections[current_section] = '\n'.join(current_content).strip()
    
    # Si no hay secciones, crear una sección por defecto
    if not sections:
        content_lines = []
        skip_first_title = False
        
        for line in lines:
            if not skip_first_title and title_pattern.match(line.strip()):
                skip_first_title = True
                continue
            content_lines.append(line)
        
        sections["Contenido"] = '\n'.join(content_lines).strip()
    
    return main_title, sections


def discover_markdown_files(directory: str) -> List[str]:
    """
    Descubre automáticamente todos los archivos .md en un directorio.
    
    Args:
        directory (str): Directorio donde buscar archivos .md
        
    Returns:
        List[str]: Lista de rutas a archivos .md encontrados
    """
    markdown_files = []
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return markdown_files
    
    md_extensions = {'.md', '.markdown', '.MD', '.Markdown'}
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(filename)
                if ext in md_extensions:
                    markdown_files.append(file_path)
        
        markdown_files.sort()
        
    except (PermissionError, OSError):
        pass
    
    return markdown_files


def discover_csv_files(directory: str) -> List[str]:
    """
    Descubre automáticamente todos los archivos .csv en un directorio.
    
    Args:
        directory (str): Directorio donde buscar archivos .csv
        
    Returns:
        List[str]: Lista de rutas a archivos .csv encontrados
    """
    csv_files = []
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return csv_files
    
    try:
        for filename in os.listdir(directory):
            if filename.lower().endswith('.csv'):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    csv_files.append(file_path)
        
        csv_files.sort()
        
    except (PermissionError, OSError):
        pass
    
    return csv_files


def get_file_info(path: str) -> Dict[str, str]:
    """
    Obtiene información básica de un archivo.
    
    Args:
        path (str): Ruta al archivo
        
    Returns:
        Dict[str, str]: Información del archivo (nombre, tamaño, etc.)
    """
    info = {
        'name': 'Desconocido',
        'size': '0 bytes',
        'exists': 'No'
    }
    
    if not os.path.exists(path):
        return info
    
    try:
        info['name'] = os.path.basename(path)
        info['exists'] = 'Sí'
        
        size_bytes = os.path.getsize(path)
        if size_bytes < 1024:
            info['size'] = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            info['size'] = f"{size_bytes / 1024:.1f} KB"
        else:
            info['size'] = f"{size_bytes / (1024 * 1024):.1f} MB"
            
    except (OSError, PermissionError):
        pass
    
    return info


def clean_markdown_content(content: str, max_length: Optional[int] = None) -> str:
    """
    Limpia y prepara contenido Markdown para renderizado.
    
    Args:
        content (str): Contenido Markdown original
        max_length (Optional[int]): Longitud máxima del contenido
        
    Returns:
        str: Contenido limpio y preparado
    """
    if not content:
        return "_Este contenido está vacío._"
    
    # Limpiar líneas vacías excesivas
    lines = content.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        line_stripped = line.strip()
        
        if not line_stripped:
            if not prev_empty:
                cleaned_lines.append('')
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    cleaned_content = '\n'.join(cleaned_lines).strip()
    
    # Truncar si es necesario
    if max_length and len(cleaned_content) > max_length:
        truncated = cleaned_content[:max_length]
        last_newline = truncated.rfind('\n')
        if last_newline > max_length * 0.8:
            truncated = truncated[:last_newline]
        
        cleaned_content = truncated + "\n\n_... (contenido truncado)_"
    
    return cleaned_content


def get_markdown_stats(content: str) -> Dict[str, int]:
    """
    Calcula estadísticas básicas de un documento Markdown.
    
    Args:
        content (str): Contenido del documento
        
    Returns:
        Dict[str, int]: Estadísticas del documento
    """
    if not content:
        return {'words': 0, 'lines': 0, 'characters': 0, 'sections': 0}
    
    lines = content.split('\n')
    words = len(content.split())
    characters = len(content)
    sections = len(re.findall(r'^##\s+', content, re.MULTILINE))
    
    return {
        'words': words,
        'lines': len(lines),
        'characters': characters,
        'sections': sections
    }