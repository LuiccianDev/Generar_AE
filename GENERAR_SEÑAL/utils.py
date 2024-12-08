import pandas as pd
from tkinter import filedialog

def save_data_to_csv(time, signal, filtered_signal, detections):
    """Guardar los datos generados en un archivo CSV usando pandas."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        # Crear un DataFrame de pandas con los datos
        data = {
            "Tiempo": time,
            "Señal Original": signal,
            "Señal Filtrada": filtered_signal,
            "Detección": detections
        }
        df = pd.DataFrame(data)
        
        # Guardar el DataFrame como un archivo CSV
        df.to_csv(file_path, index=False)
""" def save_figure_as_image(fig):
    #*Guardar la gráfica actual como imagen.
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        fig.savefig(file_path) """
        
def save_figure_as_image(fig):
    """Guardar la gráfica actual como imagen en formato PNG con opciones mejoradas."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        # Establecer la resolución (DPI) y el fondo transparente
        fig.savefig(file_path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.1)

