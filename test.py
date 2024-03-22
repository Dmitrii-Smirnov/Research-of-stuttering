from src.data_handler import DataHandler


obj = DataHandler('/Users/dmitrijsmirnov/Desktop/University/University_of_Haifa/Classes/ML/Project/data/clips_audio',
                  '/Users/dmitrijsmirnov/Desktop/University/University_of_Haifa/Classes/ML/Project/ml-stuttering-events-dataset-main/SEP-28k_labels.csv'
                  )


obj.load_metadata()
obj.load_audio_files()
