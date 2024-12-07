import csv
from tkinter import filedialog

def save_data_to_csv(time, signal, filtered_signal, detections):
    """Guardar los datos generados en un archivo CSV."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tiempo", "Señal Original", "Señal Filtrada", "Detección"])
            for i in range(len(time)):
                writer.writerow([time[i], signal[i], filtered_signal[i], detections[i]])

def save_figure_as_image(fig):
    """Guardar la gráfica actual como imagen."""
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        fig.savefig(file_path)
