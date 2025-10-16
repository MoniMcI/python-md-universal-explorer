import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import re
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class DocumentationExplorerGUI:
    def __init__(self):
        # Configurar tema moderno
        ctk.set_appearance_mode("system")  # "system", "dark", "light"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Configuración de la ventana principal
        self.root = ctk.CTk()
        self.root.title("🏪 Tienda Aurelion - Explorador de Documentación")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 600)
        # Maximizar la ventana al inicio
        self.root.state('zoomed')  # Para Windows
        
        # Variables de estado
        self.current_sections = {}
        self.current_title = ""
        self.search_results = []
        self.current_image = None
        self.current_image_path = None
        self.image_window = None
        
        # Configurar la aplicación
        self.setup_layout()
        self.load_documentation()
        
    def setup_layout(self):
        """Crear el layout principal de la aplicación."""
        # Frame principal con grid
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurar grid
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Crear sidebar y área de contenido
        self.create_sidebar()
        self.create_content_area()
        self.create_status_bar()
        
    def create_sidebar(self):
        """Crear la barra lateral de navegación."""
        # Frame de la sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=350, corner_radius=10)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.sidebar.grid_propagate(False)
        
        # Crear un frame scrolleable para toda la sidebar
        self.sidebar_scroll = ctk.CTkScrollableFrame(self.sidebar, width=330, corner_radius=8)
        self.sidebar_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la aplicación
        title_label = ctk.CTkLabel(
            self.sidebar_scroll, 
            text="🏪 Tienda Aurelion\nExplorador de Documentación",
            font=ctk.CTkFont(size=18, weight="bold"),
            justify="center"
        )
        title_label.pack(pady=(10, 20))
        
        # Sección de archivo
        file_frame = ctk.CTkFrame(self.sidebar_scroll, corner_radius=8)
        file_frame.pack(fill="x", pady=(0, 15))
        
        file_label = ctk.CTkLabel(file_frame, text="📁 Archivo", font=ctk.CTkFont(size=14, weight="bold"))
        file_label.pack(pady=(10, 5))
        
        # Dropdown para seleccionar archivo
        self.file_var = ctk.StringVar()
        self.file_dropdown = ctk.CTkComboBox(
            file_frame,
            variable=self.file_var,
            command=self.on_file_change,
            width=280
        )
        self.file_dropdown.pack(pady=(0, 10), padx=10)
        
        # Botón para cargar archivo externo
        load_btn = ctk.CTkButton(
            file_frame,
            text="📂 Cargar otro archivo",
            command=self.load_external_file,
            width=280,
            height=32
        )
        load_btn.pack(pady=(0, 10), padx=10)
        
        # Sección de navegación
        nav_frame = ctk.CTkFrame(self.sidebar_scroll, corner_radius=8)
        nav_frame.pack(fill="x", pady=(0, 15))
        
        nav_label = ctk.CTkLabel(nav_frame, text="🧭 Navegación - Secciones encontradas", font=ctk.CTkFont(size=14, weight="bold"))
        nav_label.pack(pady=(10, 5))
        
        # Frame scrolleable para las secciones (más pequeño ahora)
        self.sections_scrollframe = ctk.CTkScrollableFrame(nav_frame, width=280, height=200)
        self.sections_scrollframe.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botones de acción
        action_frame = ctk.CTkFrame(self.sidebar_scroll, corner_radius=8)
        action_frame.pack(fill="x", pady=(0, 15))
        
        action_label = ctk.CTkLabel(action_frame, text="⚡ Acciones", font=ctk.CTkFont(size=14, weight="bold"))
        action_label.pack(pady=(10, 5))
        
        # Campo de búsqueda
        self.search_entry = ctk.CTkEntry(
            action_frame,
            placeholder_text="🔍 Buscar en el documento actual...",
            width=280
        )
        self.search_entry.pack(pady=(0, 5), padx=10)
        self.search_entry.bind("<Return>", self.search_documentation)
        
        search_btn = ctk.CTkButton(
            action_frame,
            text="🔍 Buscar",
            command=self.search_documentation,
            width=280,
            height=32
        )
        search_btn.pack(pady=(0, 5), padx=10)
        
        export_btn = ctk.CTkButton(
            action_frame,
            text="💾 Exportar sección",
            command=self.export_section,
            width=280,
            height=32
        )
        export_btn.pack(pady=(0, 5), padx=10)
        
        # Switch para tema
        self.theme_switch = ctk.CTkSwitch(
            action_frame,
            text="🌙 Tema oscuro",
            command=self.toggle_theme,
            width=280
        )
        self.theme_switch.pack(pady=(5, 15), padx=10)
        
        # Configurar el estado inicial del switch basado en el tema actual
        current_mode = ctk.get_appearance_mode()
        if current_mode == "dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
        
    def create_content_area(self):
        """Crear el área principal de contenido."""
        # Frame de contenido
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Header del contenido
        self.content_header = ctk.CTkLabel(
            self.content_frame,
            text="📖 Selecciona una sección para comenzar",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        self.content_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Área de texto con scroll
        self.content_text = ctk.CTkTextbox(
            self.content_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
            corner_radius=8
        )
        self.content_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        
        # Frame para botones de imagen (inicialmente oculto)
        self.image_button_frame = ctk.CTkFrame(self.content_frame, corner_radius=8)
        self.image_button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.image_button_frame.grid_remove()  # Ocultar inicialmente
        
        # Botón para ver imagen
        self.view_image_btn = ctk.CTkButton(
            self.image_button_frame,
            text="🖼️ Ver Imagen del Diagrama",
            command=self.on_view_image_click,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.view_image_btn.pack(pady=15)
        
    def create_status_bar(self):
        """Crear barra de estado."""
        self.status_frame = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📋 Listo - Selecciona un archivo y una sección",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
    def discover_markdown_files(self):
        """Buscar archivos Markdown en el directorio docs/."""
        # Buscar en la carpeta docs del proyecto
        docs_dir = os.path.join(os.getcwd(), 'docs')
        if not os.path.exists(docs_dir):
            docs_dir = os.getcwd()  # fallback a la raíz si no existe docs
            
        md_files = []
        extensions = ['.md', '.markdown', '.MD', '.Markdown']
        
        try:
            for file in os.listdir(docs_dir):
                if any(file.endswith(ext) for ext in extensions):
                    full_path = os.path.join(docs_dir, file)
                    if os.path.isfile(full_path):
                        md_files.append(full_path)
        except PermissionError:
            pass
        
        # Ordenar con prioridad para documentacion.md
        def sort_priority(file_path):
            filename = os.path.basename(file_path).lower()
            if filename == 'documentacion.md':
                return 0  # Primera prioridad
            elif filename == 'readme.md':
                return 1  # Segunda prioridad
            else:
                return 2  # Resto en orden alfabético
        
        return sorted(md_files, key=sort_priority)
        
    def load_documentation(self):
        """Cargar la lista de archivos disponibles."""
        md_files = self.discover_markdown_files()
        
        if md_files:
            file_names = [os.path.basename(f) for f in md_files]
            self.file_dropdown.configure(values=file_names)
            self.file_dropdown.set(file_names[0])
            self.file_paths = {os.path.basename(f): f for f in md_files}
            self.on_file_change(file_names[0])
        else:
            self.file_dropdown.configure(values=["No hay archivos .md"])
            self.update_status("❌ No se encontraron archivos Markdown")
            
    def parse_markdown_sections(self, content):
        """Parsear las secciones del markdown."""
        lines = content.split('\n')
        title = ""
        sections = {}
        current_section = None
        current_content = []
        
        for line in lines:
            # Título principal (primer #)
            if line.startswith('# ') and not title:
                title = line[2:].strip()
            # Secciones principales (##)
            elif line.startswith('## '):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
                    
        # Agregar la última sección
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return title, sections
        
    def on_file_change(self, selected_file):
        """Manejar cambio de archivo seleccionado."""
        if selected_file == "No hay archivos .md":
            return
            
        file_path = self.file_paths.get(selected_file)
        if not file_path:
            return
            
        try:
            # Intentar cargar con UTF-8 primero
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
                    
            if content is None:
                raise Exception("No se pudo decodificar el archivo")
                
            # Parsear el contenido
            self.current_title, self.current_sections = self.parse_markdown_sections(content)
            
            # Actualizar la interfaz
            self.update_sections_list()
            self.update_status(f"✅ Cargado: {selected_file} ({len(self.current_sections)} secciones)")
            
            # Mostrar información del archivo
            if self.current_title:
                self.content_header.configure(text=f"📖 {self.current_title}")
                welcome_text = f"""📄 ARCHIVO CARGADO: {selected_file}

📋 TÍTULO: {self.current_title}

🔖 SECCIONES DISPONIBLES: {len(self.current_sections)}
{chr(10).join([f"  • {section}" for section in self.current_sections.keys()])}

👈 Selecciona una sección de la barra lateral para comenzar a explorar.

💡 También puedes:
  🔍 Buscar texto en la documentación
  💾 Exportar secciones a archivo
  📂 Cargar otros archivos Markdown
"""
                self.content_text.delete("1.0", "end")
                self.content_text.insert("1.0", welcome_text)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
            self.update_status(f"❌ Error cargando {selected_file}")
            
    def update_sections_list(self):
        """Actualizar la lista de secciones en la sidebar."""
        # Limpiar secciones anteriores
        for widget in self.sections_scrollframe.winfo_children():
            widget.destroy()
            
        # Crear botones para cada sección
        for section_name in self.current_sections.keys():
            # Truncar nombres largos
            display_name = section_name
            if len(display_name) > 35:
                display_name = display_name[:32] + "..."
                
            btn = ctk.CTkButton(
                self.sections_scrollframe,
                text=f"📄 {display_name}",
                command=lambda s=section_name: self.show_section(s),
                anchor="w",
                width=260,
                height=35,
                font=ctk.CTkFont(size=11)
            )
            btn.pack(pady=3, padx=5, fill="x")
            
    def show_section(self, section_name):
        """Mostrar el contenido de una sección."""
        content = self.current_sections.get(section_name, "")
        
        if content:
            # Limpiar imagen anterior y ocultar botón de imagen por defecto
            self.clear_current_image()
            self.image_button_frame.grid_remove()
            
            # Actualizar header
            self.content_header.configure(text=f"📖 {section_name}")
            
            # Formatear contenido para mejor legibilidad
            formatted_content = self.format_content(content)
            
            # Mostrar contenido
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", formatted_content)
            
            # Si hay una imagen cargada, agregar botón para verla
            if hasattr(self, 'current_image') and self.current_image:
                self.add_view_image_button()
            
            # Actualizar status
            words = len(content.split())
            lines = len(content.split('\n'))
            self.update_status(f"📖 Mostrando: {section_name} ({words} palabras, {lines} líneas)")
        else:
            messagebox.showwarning("Sección vacía", f"La sección '{section_name}' está vacía.")
    
    def add_view_image_button(self):
        """Mostrar botón para ver imagen."""
        # Mostrar el frame de botones de imagen
        self.image_button_frame.grid()
    
    def clear_current_image(self):
        """Limpiar referencia de imagen actual."""
        self.current_image = None
        self.current_image_path = None
    
    def on_view_image_click(self):
        """Manejar click del botón para ver imagen."""
        if hasattr(self, 'current_image') and self.current_image and hasattr(self, 'current_image_path'):
            self.show_image_window(self.current_image, "Diagrama de Flujo", self.current_image_path)
        else:
            messagebox.showinfo("Imagen", "No hay imagen disponible para mostrar")
            
    def format_content(self, content):
        """Formatear el contenido para mejor visualización, incluyendo imágenes."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Detectar imágenes markdown ![alt](path)
            image_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
            if image_match and PIL_AVAILABLE:
                alt_text, image_path = image_match.groups()
                # Intentar mostrar la imagen
                if self.try_display_image(image_path, alt_text):
                    formatted_lines.append(f"✅ [IMAGEN CARGADA EXITOSAMENTE: {alt_text}]")
                    formatted_lines.append(f"   📁 Archivo: {image_path}")
                    formatted_lines.append(f"   �️ Una ventana separada mostrará la imagen automáticamente")
                    # Mostrar la imagen automáticamente en ventana separada
                    self.root.after(500, lambda: self.show_image_window_if_available())
                    continue
                else:
                    formatted_lines.append(f"❌ [Imagen no encontrada: {alt_text}] - {image_path}")
                    continue
            elif image_match:  # PIL no disponible
                alt_text, image_path = image_match.groups()
                formatted_lines.append(f"🖼️ [Imagen (Pillow no instalado): {alt_text}] - {image_path}")
                continue
            
            # Convertir listas markdown a bullets
            if line.strip().startswith('- '):
                formatted_lines.append(f"  • {line.strip()[2:]}")
            elif line.strip().startswith('* '):
                formatted_lines.append(f"  • {line.strip()[2:]}")
            # Resaltar código inline
            elif '`' in line:
                # Simple highlighting para código inline
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
                
        return '\n'.join(formatted_lines)
    
    def try_display_image(self, image_path, alt_text):
        """Intentar mostrar una imagen en el área de contenido."""
        try:
            # Resolver ruta relativa desde el directorio del proyecto
            if not os.path.isabs(image_path):
                base_dir = os.getcwd()
                
                # Si la ruta empieza con ../ es relativa desde docs/
                if image_path.startswith('../'):
                    # Remover ../ y usar desde la raíz del proyecto
                    clean_path = image_path[3:]  # Quitar ../
                    full_path = os.path.join(base_dir, clean_path)
                else:
                    # Ruta relativa normal desde la raíz
                    full_path = os.path.join(base_dir, image_path)
            else:
                full_path = image_path
            
            print(f"Intentando cargar imagen: {full_path}")  # Debug
            
            if not os.path.exists(full_path):
                print(f"Imagen no encontrada en: {full_path}")  # Debug
                return False
            
            # Cargar y redimensionar imagen
            pil_image = Image.open(full_path)
            
            # Calcular tamaño para ajustar al área de contenido (máximo 800x600)
            max_width, max_height = 800, 600
            pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Convertir a formato compatible con tkinter
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Crear label para la imagen y agregarlo al content_text
            # Nota: Como CTkTextbox no soporta imágenes, las mostraremos como texto indicativo
            # y guardaremos la imagen para mostrarla en una ventana separada si es necesario
            self.show_image_in_content(tk_image, alt_text, full_path)
            
            return True
            
        except Exception as e:
            print(f"Error al cargar imagen {image_path}: {e}")
            return False
    
    def show_image_in_content(self, tk_image, alt_text, image_path):
        """Guardar referencia de imagen para uso posterior."""
        # Guardar referencia de imagen para posible uso posterior
        self.current_image = tk_image
        self.current_image_path = image_path
        
        # Actualizar status bar con información de la imagen
        self.update_status(f"🖼️ Imagen cargada: {alt_text} ({tk_image.width()}x{tk_image.height()}px)")
        
        return True
    
    def show_image_window_if_available(self):
        """Mostrar ventana de imagen si hay una imagen cargada."""
        if hasattr(self, 'current_image') and self.current_image and hasattr(self, 'current_image_path'):
            self.show_image_window(self.current_image, "Diagrama de Flujo", self.current_image_path)
    
    def show_image_window(self, tk_image, alt_text, image_path):
        """Mostrar imagen en una ventana separada."""
        if hasattr(self, 'image_window') and self.image_window and self.image_window.winfo_exists():
            self.image_window.destroy()
        
        # Crear ventana separada para la imagen
        self.image_window = ctk.CTkToplevel(self.root)
        self.image_window.title(f"🖼️ {alt_text}")
        self.image_window.geometry("1000x800")
        self.image_window.resizable(True, True)
        
        # Frame principal con scroll si es necesario
        main_frame = ctk.CTkFrame(self.image_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de la imagen
        title_label = ctk.CTkLabel(main_frame, text=f"📷 {alt_text}", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 5))
        
        # Frame para la imagen con fondo blanco
        image_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        image_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Label con la imagen
        image_label = tk.Label(image_frame, image=tk_image, bg='white')
        image_label.image = tk_image  # Mantener referencia para evitar garbage collection
        image_label.pack(padx=10, pady=10, expand=True)
        
        # Información de la imagen
        info_text = f"📁 Archivo: {os.path.basename(image_path)}\n📐 Dimensiones: {tk_image.width()} × {tk_image.height()} píxeles"
        info_label = ctk.CTkLabel(main_frame, text=info_text, 
                                 font=ctk.CTkFont(size=12))
        info_label.pack(pady=(5, 10))
        
        # Botón para cerrar
        close_button = ctk.CTkButton(main_frame, text="Cerrar", 
                                    command=self.image_window.destroy,
                                    width=100)
        close_button.pack(pady=(0, 10))
        
    def search_documentation(self, event=None):
        """Buscar texto en la documentación."""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showinfo("Búsqueda", "Ingresa un término de búsqueda")
            return
            
        results = []
        for section_name, content in self.current_sections.items():
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if search_term.lower() in line.lower():
                    results.append((section_name, line_num, line.strip()))
                    
        if results:
            # Mostrar resultados
            results_text = f"🔍 RESULTADOS DE BÚSQUEDA: '{search_term}'\n\n"
            results_text += f"Se encontraron {len(results)} coincidencias:\n\n"
            
            for section, line_num, line in results:
                results_text += f"📄 {section} (línea {line_num}):\n"
                results_text += f"   {line}\n\n"
                
            self.content_header.configure(text=f"🔍 Resultados: '{search_term}'")
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", results_text)
            self.update_status(f"🔍 Búsqueda: {len(results)} resultados para '{search_term}'")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron resultados para '{search_term}'")
            self.update_status(f"🔍 Sin resultados para '{search_term}'")
            
    def export_section(self):
        """Exportar la sección actual a archivo."""
        current_title = self.content_header.cget("text")
        if current_title.startswith("📖 Selecciona"):
            messagebox.showinfo("Exportar", "Selecciona primero una sección para exportar")
            return
            
        content = self.content_text.get("1.0", "end-1c")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Markdown", "*.md"),
                ("Todos los archivos", "*.*")
            ],
            title="Guardar sección como..."
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Exportar", f"Sección exportada a:\n{file_path}")
                self.update_status(f"💾 Exportado a {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
                
    def load_external_file(self):
        """Cargar un archivo Markdown externo."""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Archivos Markdown", "*.md *.markdown"),
                ("Todos los archivos", "*.*")
            ],
            title="Seleccionar archivo Markdown"
        )
        
        if file_path:
            try:
                # Intentar cargar el archivo
                encodings = ['utf-8', 'latin-1', 'cp1252']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                        
                if content is None:
                    raise Exception("No se pudo decodificar el archivo")
                    
                # Parsear y cargar
                self.current_title, self.current_sections = self.parse_markdown_sections(content)
                
                # Actualizar dropdown
                file_name = os.path.basename(file_path)
                current_values = list(self.file_dropdown.cget("values"))
                if file_name not in current_values:
                    current_values.append(file_name)
                    self.file_dropdown.configure(values=current_values)
                    self.file_paths[file_name] = file_path
                    
                self.file_dropdown.set(file_name)
                self.update_sections_list()
                self.update_status(f"✅ Archivo externo cargado: {file_name}")
                
                # Mostrar información
                if self.current_title:
                    self.content_header.configure(text=f"📖 {self.current_title}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
                
    def toggle_theme(self):
        """Alternar entre tema claro y oscuro."""
        # Obtener el estado del switch
        switch_state = self.theme_switch.get()
        
        if switch_state:  # Switch activado = tema oscuro
            ctk.set_appearance_mode("dark")
            new_mode = "oscuro"
        else:  # Switch desactivado = tema claro
            ctk.set_appearance_mode("light")
            new_mode = "claro"
            
        self.update_status(f"🎨 Tema cambiado a: {new_mode}")
        
        # Forzar actualización de la interfaz
        self.root.update()
        
    def update_status(self, message):
        """Actualizar la barra de estado."""
        self.status_label.configure(text=message)
        
    def run(self):
        """Ejecutar la aplicación."""
        self.root.mainloop()

def main():
    """Función principal."""
    try:
        app = DocumentationExplorerGUI()
        app.run()
    except Exception as e:
        # Fallback en caso de error con CustomTkinter
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de inicio", 
            f"No se pudo iniciar la aplicación:\n{str(e)}\n\n"
            "Asegúrate de tener CustomTkinter instalado:\n"
            "pip install customtkinter"
        )

if __name__ == "__main__":
    main()