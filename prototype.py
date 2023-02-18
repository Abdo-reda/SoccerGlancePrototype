import time
import os
import logging
from datetime import datetime
from parameters import *
from build_models.inference import invokeInference
from feature_extraction.VideoFeatureExtractor import invokeExtraction
from feature_extraction.ConvertHQtoLQ import convert_video

def main(args):

    #------ Setup of Logging & Time Stuff
    print(":)")
    start=time.time()

    # 1---- Convert from a HQ resolution to LQ ... is this needed ? ...   
    '''
    logging.info('-----------------Start Step1: Extracting Features .......')
    convert_video(args, "tests/HQ_Test.mp4", "tests/LQ_Test.mp4")
    step1 = time.time()
    logging.info(f'-----------------Time for Step1: {step1 - start} seconds')
    '''
    
    
    # 2------ Extract features
    logging.info('-----------------Start Step2: Extracting Features .......')
    invokeExtraction(args)
    step2 = time.time()
    logging.info(f'-----------------Time for Step2: {step2 - start} seconds')


    # 3------ Run Model on the extracted Features 
    logging.info('------------------Start Step3: Running Model & Getting output ........')
    invokeInference(args)
    step3 = time.time()
    logging.info(f'-----------------Time for Step3: {step3 - step2} seconds')

    logging.info(f'<-------------------------Total Time: {time.time() - start} seconds------------------->')
    


if __name__ == "__main__":
    
    #----Get Any Parameters Regarding the Input Video & Model
    args = getParameters()
    manualArg = False
    if manualArg:
        args = setManualParameters(args)

    #------Setup Logging, directory and level.
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    os.makedirs(os.path.join("models", args.model_name), exist_ok=True)
    log_path = os.path.join("models", args.model_name,
                            datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'))

    logging.basicConfig(
        level=numeric_level,
        format=
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    #----I think this sets up the values for some environment variables, this could be important ..
    if args.GPU >= 0:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.GPU)

    main(args)