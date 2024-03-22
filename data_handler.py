"""
DataHandler.py

This module contains the DataHandler class, which is responsible for loading and preprocessing audio data and
metadata for the SEP-28k dataset.
"""

import os
import librosa
import pandas as pd
from typing import Tuple
import concurrent.futures

class DataHandler:
    def __init__(self, metadata_path: str, audio_clips_directory: str, original_audio_directory: str):
        """
        Initializes the DataHandler object.

        Args:
            metadata_path (str): Path to the CSV file containing labels metadata.
            audio_clips_directory (str): Path to the directory containing audio clips.
            original_audio_directory (str): Path to the directory containing original audio files.
        """
        self.metadata_path = metadata_path
        self.audio_clips_directory = audio_clips_directory
        self.original_audio_directory = original_audio_directory
        self.metadata_df = None
        self.audio_clips_df = None
        self.original_audio_df = None

    def load_metadata(self):
        """
        Loads the metadata from the CSV file into a pandas DataFrame.
        """
        self.metadata_df = pd.read_csv(self.metadata_path)

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

    def process_audio_clips(self):
        """
        Processes audio clips and creates a DataFrame with metadata and audio data using parallel processing.
        """

        def process_clip(show, ep_id, clip_id):
            file_name = f"{show}_{ep_id}_{clip_id}.wav"
            file_path = os.path.join(self.audio_clips_directory, show, str(ep_id), file_name)
            if os.path.exists(file_path):
                y, sr = self._read_audio_file(file_path)
            else:
                y, sr = None, None
            return {
                'Show': show,
                'EpId': ep_id,
                'ClipId': clip_id,
                'AudioData': y,
                'SamplingRate': sr
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(process_clip, row.Show, row.EpId, row.ClipId)
                       for row in self.metadata_df.itertuples(index=False)]
            self.audio_clips_df = pd.DataFrame([future.result() for future in concurrent.futures.as_completed(futures)])

    def process_original_audio(self):
        """
        Processes original audio files and creates a DataFrame with unique Show, EpId,
        and processed audio data using parallel processing.
        """
        unique_shows = self.metadata_df[['Show', 'EpId']].drop_duplicates()

        def process_original(show, ep_id):
            file_name = f"{ep_id}.wav"
            file_path = os.path.join(self.original_audio_directory, show, file_name)
            if os.path.exists(file_path):
                y, sr = self._read_audio_file(file_path)
            else:
                y, sr = None, None
            return {
                'Show': show,
                'EpId': ep_id,
                'AudioData': y,
                'AudioSamplingRate': sr
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(process_original, row.Show, row.EpId)
                       for row in unique_shows.itertuples(index=False)]
            self.original_audio_df = pd.DataFrame([future.result() for future in concurrent.futures.as_completed(futures
                                                                                                                 )])


# Example usage
# data_handler = DataHandler(
#     metadata_path='path/to/metadata.csv',
#     audio_clips_directory='path/to/audio_clips',
#     original_audio_directory='path/to/original_audio'
# )
# data_handler.load_metadata()
# data_handler.process_audio_clips()
# data_handler.process_original_audio()
#
# # Access the DataFrames
# metadata_df = data_handler.metadata_df
# audio_clips_df = data_handler.audio_clips_df
# original_audio_df = data_handler.original_audio_df