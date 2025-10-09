import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import re

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
        
        # Variables de estado
        self.current_sections = {}
        self.current_title = ""
        self.search_results = []
        
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
        
        nav_label = ctk.CTkLabel(nav_frame, text="🧭 Navegación", font=ctk.CTkFont(size=14, weight="bold"))
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
        self.content_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
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
        docs_dir = os.path.join(os.getcwd(), 'docs')
        if not os.path.exists(docs_dir):
            docs_dir = os.getcwd()
            
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
            
        return sorted(md_files)
        
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
            # Actualizar header
            self.content_header.configure(text=f"📖 {section_name}")
            
            # Formatear contenido para mejor legibilidad
            formatted_content = self.format_content(content)
            
            # Mostrar contenido
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", formatted_content)
            
            # Actualizar status
            words = len(content.split())
            lines = len(content.split('\n'))
            self.update_status(f"📖 Mostrando: {section_name} ({words} palabras, {lines} líneas)")
        else:
            messagebox.showwarning("Sección vacía", f"La sección '{section_name}' está vacía.")
            
    def format_content(self, content):
        """Formatear el contenido para mejor visualización."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
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