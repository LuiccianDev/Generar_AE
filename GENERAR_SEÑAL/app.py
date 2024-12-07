import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
from signal_processing import generate_signal, bandpass_filter
from utils import save_data_to_csv, save_figure_as_image
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Señales y Gráficas")

        # Parámetros iniciales
        self.fs = 5000  # Frecuencia de muestreo
        self.duration = 5  # Duración de la señal en segundos
        self.num_emissions = 10  # Número de emisiones
        self.amplitude = 0.25  # Amplitud de la señal de ruido
        self.threshold = 0.4  # Umbral de detección
        self.speed = 50  # Intervalo de animación (ms)
        self.signal_color = 'blue'  # Color de la señal original
        self.filtered_color = 'green'  # Color de la señal filtrada
        self.detection_color = 'orange'  # Color de las detecciones
        self.threshold_color = 'red'  # Color del umbral
        self.peaks_color = 'black'  # Color de los picos (puntos altos)

        # Datos generados
        self.time = None
        self.signal = None
        self.filtered_signal = None
        self.detections = None

        # Crear contenedor de la ventana principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear la barra lateral
        self.sidebar_frame = ttk.Frame(self.root, width=200, relief="sunken", padding="10")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Crear las pestañas y controles
        self.create_sidebar()
        self.create_plot_area()

    def create_sidebar(self):
        """Crea la barra lateral con controles."""
        # Título de la barra lateral
        ttk.Label(self.sidebar_frame, text="CONTROLES DE GRAFICAS", font=("Space Mono", 14,"bold")).pack(pady=10)

        # Control de frecuencia de muestreo
        ttk.Label(self.sidebar_frame, text="FRECUENCIA DE MUESTREO (Hz):").pack(side=tk.TOP, padx=5)
        self.fs_var = tk.IntVar(value=self.fs)
        self.fs_entry = ttk.Entry(self.sidebar_frame, textvariable=self.fs_var)
        self.fs_entry.pack(side=tk.TOP, padx=5)

        # Control de duración
        ttk.Label(self.sidebar_frame, text="DURACION DE LA SENAL (s):").pack(side=tk.TOP, padx=5)
        self.duration_var = tk.DoubleVar(value=self.duration)
        self.duration_entry = ttk.Entry(self.sidebar_frame, textvariable=self.duration_var)
        self.duration_entry.pack(side=tk.TOP, padx=5)

        # Control de número de emisiones
        ttk.Label(self.sidebar_frame, text="NUMERO DE EMISIONES:").pack(side=tk.TOP, padx=5)
        self.num_emissions_var = tk.IntVar(value=self.num_emissions)
        self.num_emissions_entry = ttk.Entry(self.sidebar_frame, textvariable=self.num_emissions_var)
        self.num_emissions_entry.pack(side=tk.TOP, padx=5)

        # Control de amplitud
        ttk.Label(self.sidebar_frame, text="AMPLITUD DEL RUIDO:").pack(side=tk.TOP, padx=5)
        self.amplitude_var = tk.DoubleVar(value=self.amplitude)
        self.amplitude_entry = ttk.Entry(self.sidebar_frame, textvariable=self.amplitude_var)
        self.amplitude_entry.pack(side=tk.TOP, padx=5)

        # Control de velocidad
        ttk.Label(self.sidebar_frame, text="VELOCIDAD (ms entre frames):").pack(side=tk.TOP, padx=5)
        self.speed_var = tk.IntVar(value=self.speed)
        self.speed_entry = ttk.Entry(self.sidebar_frame, textvariable=self.speed_var)
        self.speed_entry.pack(side=tk.TOP, padx=5)

        # Control de umbral
        ttk.Label(self.sidebar_frame, text="UMBRAL DE DETECCION:").pack(side=tk.TOP, padx=5)
        self.threshold_var = tk.DoubleVar(value=self.threshold)
        self.threshold_entry = ttk.Entry(self.sidebar_frame, textvariable=self.threshold_var)
        self.threshold_entry.pack(side=tk.TOP, padx=5)

        # Botón para generar datos
        self.generate_button = ttk.Button(self.sidebar_frame, text="GENERAR DATOS", command=self.generate_and_plot)
        self.generate_button.pack(side=tk.TOP, pady=10)

        # Selección de gráfica
        ttk.Label(self.sidebar_frame, text="SELECCION DE GRÁFICA:").pack(side=tk.TOP, padx=5)
        self.graph_selection = tk.StringVar(value="All")
        self.graph_selector = ttk.Combobox(self.sidebar_frame, textvariable=self.graph_selection, values=["All", "SEÑAL ORIGINAL", "SEÑAL FILTRADA", "SEÑALES DETECTADAS"])
        self.graph_selector.pack(side=tk.TOP, padx=5)
        
        # Asociar el evento de selección del desplegable con el método de actualización
        self.graph_selector.bind("<<ComboboxSelected>>", self.update_graph)

        # Botones para cambiar colores
        ttk.Button(self.sidebar_frame, text="COLOR SEÑAL ORIGINAL", command=self.choose_signal_color).pack(side=tk.TOP, pady=5)
        ttk.Button(self.sidebar_frame, text="COLOR SEÑAL FILTRADA", command=self.choose_filtered_color).pack(side=tk.TOP, pady=5)
        ttk.Button(self.sidebar_frame, text="COLOR DETECCION", command=self.choose_detection_color).pack(side=tk.TOP, pady=5)
        ttk.Button(self.sidebar_frame, text="COLOR UMBRAL", command=self.choose_threshold_color).pack(side=tk.TOP, pady=5)
        ttk.Button(self.sidebar_frame, text="COLOR PICOS", command=self.choose_peaks_color).pack(side=tk.TOP, pady=5)

    def create_plot_area(self):
        """Crea el área de la gráfica dentro de la ventana principal."""
        # Frame para la gráfica
        plot_frame = ttk.Frame(self.main_frame, padding="10")
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear figura de Matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Embedding de Matplotlib en Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def choose_signal_color(self):
        """Abrir el selector de color para la señal original."""
        color = colorchooser.askcolor()[1]
        if color:
            self.signal_color = color

    def choose_filtered_color(self):
        """Abrir el selector de color para la señal filtrada."""
        color = colorchooser.askcolor()[1]
        if color:
            self.filtered_color = color

    def choose_detection_color(self):
        """Abrir el selector de color para las detecciones."""
        color = colorchooser.askcolor()[1]
        if color:
            self.detection_color = color

    def choose_threshold_color(self):
        """Abrir el selector de color para el umbral."""
        color = colorchooser.askcolor()[1]
        if color:
            self.threshold_color = color

    def choose_peaks_color(self):
        """Abrir el selector de color para los picos (puntos altos)."""
        color = colorchooser.askcolor()[1]
        if color:
            self.peaks_color = color

    def generate_and_plot(self):
        """Generar los datos y actualizar la gráfica."""
        # Leer los nuevos valores de los parámetros
        self.fs = self.fs_var.get()
        self.duration = self.duration_var.get()
        self.num_emissions = self.num_emissions_var.get()
        self.amplitude = self.amplitude_var.get()
        self.speed = self.speed_var.get()
        self.threshold = self.threshold_var.get()

        # Regenerar la señal con los nuevos parámetros
        self.time, self.signal, self.filtered_signal, self.detections = generate_signal(self.fs, self.duration, self.num_emissions, self.amplitude, self.threshold)

        # Limpiar el eje (canvas) antes de redibujar
        self.ax.clear()

        # Establecer límites automáticos según los datos generados
        self.ax.set_xlim([self.time[0], self.time[-1]])

        # Establecer el título para la gráfica
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Amplitud")
        self.ax.grid()

        # Controlar la visibilidad de las gráficas
        self.control_visibility()

        # Actualizar el canvas
        self.canvas.draw()

    def update_graph(self, event=None):
        """Actualiza la gráfica según la selección del desplegable."""
        # Limpiar la gráfica antes de redibujar
        self.ax.clear()

        # Establecer límites automáticos según los datos generados
        self.ax.set_xlim([self.time[0], self.time[-1]])

        # Establecer el título
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Amplitud")
        self.ax.grid()

        # Determinar qué graficar según la selección
        selection = self.graph_selection.get()

        if selection == "Señal Original" or selection == "All":
            self.ax.plot(self.time, self.signal, label="Señal Original", color=self.signal_color)
        if selection == "Señal Filtrada" or selection == "All":
            self.ax.plot(self.time, self.filtered_signal, label="Señal Filtrada", color=self.filtered_color)
        if selection == "Detección" or selection == "All":
            self.ax.plot(self.time, self.detections, label="Detección", color=self.detection_color)

        self.ax.legend()

        # Actualizar el canvas con la nueva gráfica
        self.canvas.draw()

    def control_visibility(self):
        """Controla la visibilidad de las gráficas según la selección del usuario."""
        selection = self.graph_selection.get()

        # Controlar la visibilidad de las gráficas
        if selection == "All":
            self.ax.plot(self.time, self.signal, label="Señal Original", color=self.signal_color)
            self.ax.plot(self.time, self.filtered_signal, label="Señal Filtrada", color=self.filtered_color)
            self.ax.plot(self.time, self.detections, label="Detección", color=self.detection_color)
        elif selection == "Señal Original":
            self.ax.plot(self.time, self.signal, label="Señal Original", color=self.signal_color)
        elif selection == "Señal Filtrada":
            self.ax.plot(self.time, self.filtered_signal, label="Señal Filtrada", color=self.filtered_color)
        elif selection == "Detección":
            self.ax.plot(self.time, self.detections, label="Detección", color=self.detection_color)

        self.ax.legend()
        self.canvas.draw()

    def save_data(self):
        """Guardar los datos generados en un archivo CSV."""
        save_data_to_csv(self.time, self.signal, self.filtered_signal, self.detections)

    def save_image(self):
        """Guardar la gráfica actual como imagen."""
        save_figure_as_image(self.fig)

    def run(self):
        self.root.mainloop()
