import streamlit as st
from pydub import AudioSegment
import librosa

import numpy as np
from rich import print


def check_audio_conditions_with_librosa(file_path):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)

    # Check the duration
    duration = librosa.get_duration(y=y, sr=sr)
    if duration > 60:  # Duration in seconds
        return "O arquivo de áudio deve ter menos de um minuto de duração."

    # Calculate the average loudness in dB
    rms = np.sqrt(np.mean(y**2))
    db = 20 * np.log10(rms)

    threshold_dB = -50.0  # Ajustado para -50 dB com base na diretriz da OMS.

    if db < threshold_dB:
        return f"O arquivo de áudio não excede o limite de {threshold_dB} decibéis recomendado pela OMS e não pode ser considerado poluição sonora."

    return None
