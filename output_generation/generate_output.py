import os
import logging
#from feature_extractor import buildFeatureExtractor, buildPCAReducer
import sys
import time
sys.path.append('/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype')
from configuration import Configuration
from build_models.inference import generateOutput, buildModel


MODEL = None
OUTPUT_PATH = None
CHUNK_SIZE = 5

def process_input(inference_configuration):
    video_path = inference_configuration['input_path']
    chunk_num = 0
    while True:
        files = os.listdir(video_path)
        added = [file for file in files if file.endswith('.npy')]
        for file in added:
            input_path = video_path + file
            time.sleep(1) # wait for the file to be fully copied to the input folder
            generate_output(input_path, chunk_num, inference_configuration)
            chunk_num+= 1
            os.remove(input_path)


def generate_output(input_path, chunk_num, inference_configuration):
    # generate outputs
    inference_configuration['input_path'] = input_path
    generateOutput(MODEL, inference_configuration,  chunk_num, CHUNK_SIZE)
    


def main():
    myConfiguration = Configuration()
    args = myConfiguration.get_configuration()
    global MODEL
    global OUTPUT_PATH
    MODEL = buildModel(args['model_configuration'])
    OUTPUT_PATH = args['inference_configuration']['output_path']
    process_input(args['inference_configuration'])
    return


if __name__ == "__main__":
    main()

