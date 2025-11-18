import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from algorithms.path_finder import PathFinder
from ui.graph_visualizer import GraphVisualizer

class TkInterface:
    def __init__(self):
        self.finder = PathFinder()
        self.visualizer = GraphVisualizer()

        # Destination options
        self.classes = ["5012", "5014", "5411", "INPUT"]
        self.names = ["🍻 Cervecería Mi Rolita", "💃 Discoteca The Darkness",
                      "🎵 Bar La Pasión", "📍 Otro Destino (Ingresar)"]

        self.root = None
        self.result_text = None
        self.style = None
        
   
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'background': '#F5F5F5',
            'card_bg': '#FFFFFF',
            'text_dark': '#2C3E50',
            'success': '#27AE60',
            'warning': '#E67E22'
        }

    def setup_styles(self):
        """Configura estilos modernos para la interfaz"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
   
        self.style.configure('Primary.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Arial', 10, 'bold'),
                           padding=(15, 8))
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['secondary'],
                           foreground='white',
                           font=('Arial', 10),
                           padding=(12, 6))
        
        self.style.configure('Title.TLabel',
                           font=('Arial', 16, 'bold'),
                           foreground=self.colors['text_dark'])
        
        self.style.configure('Subtitle.TLabel',
                           font=('Arial', 12, 'bold'),
                           foreground=self.colors['primary'])

    def _get_dynamic_destination(self):
        """Diálogo mejorado para ingresar destino personalizado"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Destino Personalizado")
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['background'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_x() + 100, self.root.winfo_y() + 100))
        
        ttk.Label(dialog, text="Ingrese las coordenadas", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para calle
        calle_frame = ttk.Frame(dialog)
        calle_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(calle_frame, text="Calle (50-55):").pack(side='left')
        calle_var = tk.StringVar()
        calle_combo = ttk.Combobox(calle_frame, textvariable=calle_var,
                                  values=[str(i) for i in range(50, 56)], 
                                  state="readonly", width=8)
        calle_combo.pack(side='right')
        calle_combo.set('50')
        
        # Frame para carrera
        carrera_frame = ttk.Frame(dialog)
        carrera_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(carrera_frame, text="Carrera (10-15):").pack(side='left')
        carrera_var = tk.StringVar()
        carrera_combo = ttk.Combobox(carrera_frame, textvariable=carrera_var,
                                    values=[str(i) for i in range(10, 16)], 
                                    state="readonly", width=8)
        carrera_combo.pack(side='right')
        carrera_combo.set('10')
        
        result = [None]  # Para capturar el resultado
        
        def on_ok():
            if calle_var.get() and carrera_var.get():
                result[0] = f"{calle_var.get()}{carrera_var.get()}"
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia", "Complete ambos campos")
        
        def on_cancel():
            dialog.destroy()
        
        # Botones
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Aceptar", command=on_ok,
                  style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=on_cancel,
                  style='Secondary.TButton').pack(side='left', padx=5)
        
        dialog.wait_window()
        return result[0]

    def _show_result(self, text: str):
        """Muestra resultados con formato mejorado"""
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        
        # Aplicar formato básico al texto
        formatted_text = self._format_result_text(text)
        self.result_text.insert(tk.END, formatted_text)
        
        # Aplicar tags para colores
        self._apply_text_tags(text)
        self.result_text.config(state='disabled')
        
        # Auto-scroll al inicio
        self.result_text.see('1.0')

    def _format_result_text(self, text: str) -> str:
        """Da formato al texto de resultados"""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if 'Destino:' in line:
                formatted_lines.append(f"🎯 {line}")
            elif 'Javier' in line and 'minutos' in line:
                formatted_lines.append(f"👨 {line}")
            elif 'Andreína' in line and 'minutos' in line:
                formatted_lines.append(f"👩 {line}")
            elif 'Para sincronizar' in line:
                formatted_lines.append(f"⏰ {line}")
            elif 'Ambos deben salir' in line:
                formatted_lines.append(f"✅ {line}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)

    def _apply_text_tags(self, text: str):
        """Aplica colores y estilos al texto"""
        # Configurar tags
        self.result_text.tag_configure('destino', foreground=self.colors['primary'], 
                                      font=('Arial', 11, 'bold'))
        self.result_text.tag_configure('javier', foreground='#E74C3C')
        self.result_text.tag_configure('andreina', foreground='#27AE60')
        self.result_text.tag_configure('recomendacion', foreground=self.colors['warning'],
                                      font=('Arial', 10, 'bold'))
        
        # Aplicar tags
        content = self.result_text.get('1.0', tk.END)
        if 'Destino:' in content:
            start_idx = content.find('Destino:')
            end_idx = content.find('\n', start_idx)
            if end_idx == -1:
                end_idx = 'end'
            self.result_text.tag_add('destino', f'1.0+{start_idx}c', f'1.0+{end_idx}c')
        
        # Buscar y aplicar otros tags...
        lines = content.split('\n')
        current_pos = 0
        for line in lines:
            if 'Javier' in line and 'minutos' in line:
                start_idx = current_pos + line.find('Javier')
                end_idx = current_pos + len(line)
                self.result_text.tag_add('javier', f'1.0+{start_idx}c', f'1.0+{end_idx}c')
            elif 'Andreína' in line and 'minutos' in line:
                start_idx = current_pos + line.find('Andreína')
                end_idx = current_pos + len(line)
                self.result_text.tag_add('andreina', f'1.0+{start_idx}c', f'1.0+{end_idx}c')
            elif 'Para sincronizar' in line or 'Ambos deben salir' in line:
                start_idx = current_pos
                end_idx = current_pos + len(line)
                self.result_text.tag_add('recomendacion', f'1.0+{start_idx}c', f'1.0+{end_idx}c')
            
            current_pos += len(line) + 1  

    def on_show_route(self):
        """Manejador mejorado para calcular rutas"""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Selección Requerida", 
                                 "Por favor seleccione un destino de la lista")
            return

        index = sel[0]
        dest_flag = self.classes[index]
        dest_name = self.names[index]

        # Mostrar indicador de progreso
        self.progress_bar.start()
        self.calculate_btn.config(state='disabled')

        def calculate():
            try:
                if dest_flag == 'INPUT':
                    final_id = self._get_dynamic_destination()
                    if final_id is None:
                        return
                else:
                    final_id = dest_flag

                graphJ, graphA, timeJ, timeA = self.finder.find_optimal_paths(final_id)
                
                # Actualizar UI en el hilo principal
                self.root.after(0, lambda: self._display_results(
                    graphJ, graphA, final_id, dest_name, timeJ, timeA
                ))
                
            except KeyError:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", "El destino seleccionado no existe en el mapa"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"Error al calcular las rutas:\n{str(e)}"))
            finally:
                self.root.after(0, self._calculation_finished)

        # Ejecutar en un hilo separado para no bloquear la UI
        import threading
        thread = threading.Thread(target=calculate)
        thread.daemon = True
        thread.start()

    def _display_results(self, graphJ, graphA, final_id, dest_name, timeJ, timeA):
        """Muestra los resultados del cálculo"""
        res = f"📍 DESTINO: {dest_name.replace('🍻', '').replace('💃', '').replace('🎵', '').replace('📍', '').strip()}\n"
        res += f"   Coordenadas: Calle {final_id[0:2]} con Carrera {final_id[2:4]}\n\n"
        
        res += "👨 JAVIER\n"
        res += f"   ⏱️  Tiempo: {timeJ} minutos\n"
        res += "   🛣️  Ruta:\n   "
        res += self.finder.shortest_path(graphJ, graphJ.nodes_dict[final_id]).replace('==>', '\n   ==>') + '\n\n'
        
        res += "👩 ANDREÍNA\n"
        res += f"   ⏱️  Tiempo: {timeA} minutos\n"
        res += "   🛣️  Ruta:\n   "
        res += self.finder.shortest_path(graphA, graphA.nodes_dict[final_id]).replace('==>', '\n   ==>') + '\n\n'

        # Recomendación
        res += "💡 RECOMENDACIÓN DE SALIDA\n"
        if timeJ > timeA:
            res += f"   Andreína debe salir {timeJ - timeA} minutos después de Javier\n"
        elif timeA > timeJ:
            res += f"   Javier debe salir {timeA - timeJ} minutos después de Andreína\n"
        else:
            res += "   Ambos deben salir al mismo tiempo\n"

        self._show_result(res)

        # Guardar para visualización
        self._last_graphJ = graphJ
        self._last_graphA = graphA
        self._last_destination = final_id
        
        # Habilitar botón de visualización
        self.visualize_btn.config(state='normal')

    def _calculation_finished(self):
        """Limpia después del cálculo"""
        self.progress_bar.stop()
        self.calculate_btn.config(state='normal')

    def on_visualize(self):
        """Manejador para visualización con diálogo de confirmación"""
        if not hasattr(self, '_last_graphJ'):
            messagebox.showwarning("Sin Datos", 
                                 "Primero calcule una ruta para poder visualizarla")
            return
        
        response = messagebox.askyesno("Visualizar Mapa", 
                                      "¿Desea abrir la visualización del mapa?\n\n"
                                      "Esto abrirá una ventana separada con la representación gráfica de las rutas.")
        if response:
            try:
                path_javier = self.visualizer.path_to_node_list(self._last_graphJ, self._last_destination)
                path_andreina = self.visualizer.path_to_node_list(self._last_graphA, self._last_destination)
                
                self.visualizer.visualize(self._last_graphJ, self._last_graphA, 
                                        self._last_destination, path_javier, path_andreina)
            except Exception as e:
                messagebox.showerror("Error de Visualización", 
                                   f"No se pudo generar la visualización:\n{str(e)}")

    def create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Título principal
        title_label = ttk.Label(header_frame, 
                               text="🗺️ Sistema de Rutas - Bogotá", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(header_frame,
                                  text="Calcula las rutas óptimas para Javier y Andreína",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()

    def create_destination_section(self, parent):
        """Crea la sección de selección de destino"""
        dest_frame = ttk.LabelFrame(parent, text=" 🎯 Seleccionar Destino ", 
                                   padding="15", style='Card.TFrame')
        dest_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(dest_frame, text="Elija un destino de la lista:").pack(anchor='w')
        
        # Listbox con scroll
        listbox_frame = ttk.Frame(dest_frame)
        listbox_frame.pack(fill='x', pady=10)
        
        self.listbox = tk.Listbox(listbox_frame, height=6, font=('Arial', 10),
                                 selectbackground=self.colors['primary'])
        self.listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', 
                                 command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        for name in self.names:
            self.listbox.insert(tk.END, name)
        
        # Seleccionar el primer elemento por defecto
        self.listbox.selection_set(0)

    def create_controls_section(self, parent):
        """Crea la sección de controles"""
        controls_frame = ttk.Frame(parent, style='Card.TFrame')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(controls_frame, mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # Botones
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(fill='x')
        
        self.calculate_btn = ttk.Button(btn_frame, text="🚀 Calcular Ruta Óptima", 
                                       command=self.on_show_route,
                                       style='Primary.TButton')
        self.calculate_btn.pack(side='left', padx=(0, 10))
        
        self.visualize_btn = ttk.Button(btn_frame, text="📊 Visualizar Mapa", 
                                       command=self.on_visualize,
                                       style='Secondary.TButton')
        self.visualize_btn.pack(side='left', padx=(0, 10))
        self.visualize_btn.config(state='disabled')  # Inicialmente deshabilitado
        
        ttk.Button(btn_frame, text="🔄 Limpiar", 
                  command=self.clear_results).pack(side='left', padx=(0, 10))
        
        ttk.Button(btn_frame, text="❌ Salir", 
                  command=self.root.quit).pack(side='right')

    def create_results_section(self, parent):
        """Crea la sección de resultados"""
        results_frame = ttk.LabelFrame(parent, text=" 📋 Resultados ", 
                                      padding="15", style='Card.TFrame')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.result_text = ScrolledText(results_frame, width=80, height=20, 
                                       wrap='word', font=('Consolas', 10),
                                       bg='#FAFAFA', relief='solid', bd=1)
        self.result_text.pack(fill='both', expand=True)
        self.result_text.config(state='disabled')

    def clear_results(self):
        """Limpia los resultados"""
        self._show_result("")
        if hasattr(self, '_last_graphJ'):
            del self._last_graphJ
        if hasattr(self, '_last_graphA'):
            del self._last_graphA
        self.visualize_btn.config(state='disabled')

    def build_ui(self):
        """Construye la interfaz de usuario completa"""
        self.setup_styles()
        
        # Configurar ventana principal
        self.root.title('🗺️ Sistema de Rutas - Bogotá')
        self.root.geometry('900x700')
        self.root.minsize(800, 600)
        self.root.configure(bg=self.colors['background'])
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="0", style='TFrame')
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Configurar grid para responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Crear secciones
        self.create_header(main_frame)
        self.create_destination_section(main_frame)
        self.create_controls_section(main_frame)
        self.create_results_section(main_frame)
        
        # Mensaje inicial
        initial_message = """🌟 BIENVENIDO AL SISTEMA DE RUTAS BOGOTÁ 🌟

Instrucciones:
1. Seleccione un destino de la lista
2. Haga clic en 'Calcular Ruta Óptima'
3. Revise los resultados y tiempos
4. Visualice el mapa si lo desea

El sistema calculará los mejores caminos para:
• 🚶 Javier (Calle 54, Carrera 14)
• 🚶♀️ Andreína (Calle 52, Carrera 13)

¡Comience seleccionando un destino y calculando la ruta!"""
        
        self._show_result(initial_message)

    def run(self):
        """Ejecuta la aplicación"""
        self.root = tk.Tk()
        try:
            self.build_ui()
            # Centrar ventana
            self.root.eval('tk::PlaceWindow . center')
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")
        finally:
            # Clean up
            if hasattr(self, 'root'):
                self.root.quit()

