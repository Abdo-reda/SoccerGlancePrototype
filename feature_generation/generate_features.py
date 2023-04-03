import os
import logging
#from feature_extractor import buildFeatureExtractor, buildPCAReducer
import sys
import time
import shutil 
sys.path.append('/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype')
from configuration import Configuration
from feature_generation.feature_extractor import buildFeatureExtractor
import psutil

FEATURE_EXTRACTOR = None
OUTPUT_PATH = None
CHUNK_SIZE = 5.0
TEMP_PROCESSED_PATH = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/chunk_generation/generated_chunks/proccessed_chunks/'
PID = None

def process_input(feature_configuration):
    video_path = feature_configuration['input_path']
    chunk_num = 0
    process_handle = psutil.Process(PID)
    while True:
        files = os.listdir(video_path)
        added = [file for file in files if file.endswith('.mp4')]
        for file in added:
            input_path = video_path + file
            is_file_use = True
                
            while is_file_use:     
                file_handles = process_handle.open_files()
                for fh in file_handles:
                    if(input_path == fh.path):
                        is_file_use = True 
                        break
                    is_file_use = False
                pass
            
            
            moved_path = TEMP_PROCESSED_PATH + file
            generate_features(input_path, chunk_num)
            chunk_num += 1
            shutil.move(input_path, moved_path)


def generate_features(input_path, chunk_num):
    
    output_path = OUTPUT_PATH + 'feature_chunk_' + str(chunk_num)
    # extract features ...
    FEATURE_EXTRACTOR.feature_extractor.extractFeatures(
        path_video_input = input_path,
        path_features_output = output_path,
        start = 0.0,
        duration = CHUNK_SIZE,
        overwrite = True
    )

    feature_path = output_path + '.npy'
    # reduce features ...
    if FEATURE_EXTRACTOR.feature_reducer:
        FEATURE_EXTRACTOR.feature_reducer.reduceFeatures(
            input_features=feature_path,
            output_features=feature_path,
            overwrite=True
        )


def main():
    myConfiguration = Configuration()
    args = myConfiguration.get_configuration()
    global FEATURE_EXTRACTOR
    global OUTPUT_PATH
    global PID
    PID = int(sys.argv[1])
    FEATURE_EXTRACTOR = buildFeatureExtractor(args['feature_configuration'])
    OUTPUT_PATH = args['feature_configuration']['output_path']
    process_input(args['feature_configuration'])
    return


if __name__ == "__main__":
    main()

