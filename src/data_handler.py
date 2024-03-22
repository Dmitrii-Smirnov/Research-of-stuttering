"""
DataHandler.py

This module contains the DataHandler class, which is responsible for loading and preprocessing audio data and
metadata for the SEP-28k dataset.
"""

import os
import json
import librosa
import numpy as np
import pandas as pd
from typing import Tuple
import concurrent.futures


class DataHandler:
    """
    A class for handling the loading and preprocessing of audio data and metadata for the SEP-28k dataset.
    """

    def __init__(self, data_directory: str, labels_metadata_path: str):
        """
        Initializes the DataHandler object.

        Args:
            data_directory (str): Path to the directory containing audio files.
            labels_metadata_path (str): Path to the CSV file containing labels metadata.
        """
        self.data_directory = data_directory
        self.labels_metadata_path = labels_metadata_path
        self.labels_metadata = None

    def _read_audio_file(self, file_path: str) -> Tuple[str, bytes]:
        """
        Reads an audio file using librosa.

        Args:
            file_path (str): Path to the audio file.

        Returns:
            Tuple[str, bytes]: The audio time series and sampling rate, or (None, None) if an error occurs.
        """
        try:
            y, sr = librosa.load(file_path, sr=None)
            return y, sr
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None, None

    def load_metadata(self):
        """
        Loads the metadata from the CSV file into a pandas DataFrame.
        """
        self.labels_metadata = pd.read_csv(self.labels_metadata_path)

    def load_audio_files(self):
        """
        Recursively loads audio files listed in the labels metadata and updates the DataFrame with
        the audio data using parallel processing.
        """
        audio_file_paths = {}
        for root, dirs, files in os.walk(self.data_directory):
            for file in files:
                if file.endswith('.wav'):
                    audio_file_paths[file] = os.path.join(root, file)

        def process_audio_file(index, row):
            file_name = f"{row['Show']}_{row['EpId']}_{row['ClipId']}.wav"
            if file_name in audio_file_paths:
                y, sr = self._read_audio_file(audio_file_paths[file_name])
                return index, json.dumps(np.array(y).tolist()), sr
            return index, None, None

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(process_audio_file, index, row)
                       for index, row in self.labels_metadata.iterrows()]
            for future in concurrent.futures.as_completed(futures):
                index, audio_data, sr = future.result()
                self.labels_metadata.at[index, 'ClipsAudioData'] = audio_data
                self.labels_metadata.at[index, 'ClipsSamplingRate'] = sr
