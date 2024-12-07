import numpy as np
from scipy.signal import butter, filtfilt

def generate_signal(fs, duration, num_emissions, amplitude, threshold):
    """Genera la señal simulada con ruido y emisiones acústicas."""
    time = np.linspace(0, duration, int(fs * duration), endpoint=False)
    noise = amplitude * np.random.randn(len(time))
    signal = np.copy(noise)

    # Simular emisiones acústicas
    emission_times = np.random.choice(time, size=num_emissions, replace=False)
    for t in emission_times:
        index = np.argmin(np.abs(time - t))
        pulse = np.sin(2 * np.pi * 1000 * time[index:index + 100])
        signal[index:index + 100] += pulse

    # Filtrar la señal
    filtered_signal = bandpass_filter(signal, lowcut=800, highcut=1200, fs=fs)

    # Detección de emisiones (simple umbral)
    detections = (filtered_signal > threshold).astype(int)

    return time, signal, filtered_signal, detections

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """Filtra la señal con un filtro paso banda."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    return filtfilt(b, a, data)
