"""
This file contains functions for creating static plots, such as time series plots.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_time_series(audio_clips_df, output_directory, show, ep_id, clip_id):
    """
    Plots the time series of an audio clip.

    Args:
        audio_clips_df (pd.DataFrame): DataFrame containing audio clips data.
        output_directory (str): Path to the directory where the plot will be saved.
        show (str): Show identifier.
        ep_id (int): Episode identifier.
        clip_id (int): Clip identifier.
    """
    clip = audio_clips_df[(audio_clips_df['Show'] == show) &
                          (audio_clips_df['EpId'] == ep_id) &
                          (audio_clips_df['ClipId'] == clip_id)]

    if not clip.empty:
        audio_data = clip.iloc[0]['AudioData']
        plt.figure(figsize=(10, 4))
        plt.plot(audio_data)
        plt.title(f'Time Series Plot - Show: {show}, EpId: {ep_id}, ClipId: {clip_id}')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.savefig(f'{output_directory}/time_series_plot_{show}_{ep_id}_{clip_id}.png')
        plt.close()
    else:
        print(f'No audio clip found for Show: {show}, EpId: {ep_id}, ClipId: {clip_id}')
