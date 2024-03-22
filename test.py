from src.data_handler import DataHandler


data_handler = DataHandler(
    metadata_path='/Users/dmitrijsmirnov/Desktop/University/University_of_Haifa/Classes/ML/Project/ml-stuttering-events-dataset-main/SEP-28k_labels.csv',
    audio_clips_directory='/Users/dmitrijsmirnov/Desktop/University/University_of_Haifa/Classes/ML/Project/data/clips_audio',
    original_audio_directory='/Users/dmitrijsmirnov/Desktop/University/University_of_Haifa/Classes/ML/Project/data/audio'
)
data_handler.load_metadata()
data_handler.process_audio_clips()
data_handler.process_original_audio()

# Access the DataFrames
metadata_df = data_handler.metadata_df
audio_clips_df = data_handler.audio_clips_df
original_audio_df = data_handler.original_audio_df