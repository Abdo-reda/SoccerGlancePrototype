import os
import logging
#from feature_extractor import buildFeatureExtractor, buildPCAReducer
import sys
import time
sys.path.append('/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype')
from configuration import Configuration
from build_models.inference import generateOutput, buildModel
import psutil


MODEL = None
OUTPUT_PATH = None
CHUNK_SIZE = 5
PID = None

def process_input(inference_configuration):
    video_path = inference_configuration['input_path']
    chunk_num = 0
    process_handle = psutil.Process(PID)
    while True:
        files = os.listdir(video_path)
        added = [file for file in files if file.endswith('.npy')]
        for file in added:
            input_path = video_path + file
            is_file_use = True
                
            while is_file_use:     
                file_handles = process_handle.open_files()
                # print('---------------------------------------', file_handles)
                for fh in file_handles:
                    if(input_path == fh.path):
                        is_file_use = True 
                        break
                    is_file_use = False
                pass
            
            generate_output(input_path, chunk_num, inference_configuration)
            chunk_num+= 1
            os.remove(input_path)


def generate_output(input_path, chunk_num, inference_configuration):
    inference_configuration['input_path'] = input_path
    generateOutput(MODEL, inference_configuration,  chunk_num, CHUNK_SIZE)
    


def main():
    myConfiguration = Configuration()
    args = myConfiguration.get_configuration()
    global MODEL
    global OUTPUT_PATH
    global PID
    PID = int(sys.argv[1])
    MODEL = buildModel(args['model_configuration'])
    OUTPUT_PATH = args['inference_configuration']['output_path']
    process_input(args['inference_configuration'])
    return


if __name__ == "__main__":
    main()

