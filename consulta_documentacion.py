#!/usr/bin/env python3
"""
Consulta de documentación - TIENDA AURELION
Script simplificado para explorar la documentación con formato limpio.
"""

import os
import sys
import textwrap


def get_base_config():
    """Configuración base: directorio y ruta de documentación."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    doc_path = os.path.join(base_dir, 'docs', 'documentacion.md')
    return base_dir, doc_path


def load_documentation(path):
    """Carga DOCUMENTACION.md y devuelve (texto_completo, secciones_dict)."""
    if not os.path.exists(path):
        return '', {}
    
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    sections = {}
    current = None
    
    for line in text.splitlines():
        if line.startswith('## '):
            current = line[3:].strip()
            sections[current] = []
        else:
            if current is not None:
                sections[current].append(line)
    
    for k in list(sections.keys()):
        sections[k] = '\n'.join(sections[k]).strip()
    
    return text, sections


def display_section_formatted(title, content):
    """Muestra una sección con formato simple y limpio."""
    # Título claro
    print(f"\n{'='*60}")
    print(f"📖 {title}")
    print(f"{'='*60}")
    print()
    
    # Mostrar todo el contenido - el scroll natural de la terminal se encarga del resto
    print(content)
    
    print(f"\n{'='*60}")
    print("Presiona Enter para continuar...")


def display_menu(sections):
    """Muestra el menú principal de secciones."""
    print("\n============================================================")
    print("🏪 CONSULTA DE DOCUMENTACIÓN - TIENDA AURELION")
    print("============================================================")
    
    print("\n📚 Secciones disponibles:")
    print("-" * 30)
    
    section_list = list(sections.keys())
    for i, title in enumerate(section_list, 1):
        # Remover contenido entre paréntesis para mostrar solo el título limpio
        clean_title = title.split('(')[0].strip()
        print(f"{i:2d}. {clean_title}")
    
    print(f"{len(section_list)+1:2d}. ❌ Salir")


def run_interactive():
    """Ejecuta el modo interactivo del programa."""
    base_dir, doc_path = get_base_config()
    
    # Cargar documentación
    text, sections = load_documentation(doc_path)
    if not text:
        print(f"❌ Error: No se encontró el archivo de documentación.")
        print(f"   Ruta esperada: {doc_path}")
        print(f"   Directorio base: {base_dir}")
        return
    
    print(f"✅ Documentación cargada exitosamente desde:")
    print(f"   {doc_path}")
    print(f"   Secciones encontradas: {len(sections)}")
    
    section_list = list(sections.keys())
    
    while True:
        display_menu(sections)
        
        try:
            choice = input("\n🔍 Selecciona una opción (número): ").strip()
            
            if choice == str(len(section_list) + 1) or choice.lower() in ('q', 'salir', 'exit'):
                print("\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
                break
            
            try:
                idx = int(choice)
                if 1 <= idx <= len(section_list):
                    sec = section_list[idx - 1]
                    content = sections.get(sec, '')
                    display_section_formatted(sec, content)
                    input("\n⏸️  Presiona Enter para continuar...")
                else:
                    print("❌ Número fuera de rango. Intente de nuevo.")
            except ValueError:
                print("❌ Por favor ingrese un número válido.")
                
        except KeyboardInterrupt:
            print("\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
            break


if __name__ == "__main__":
    run_interactive()