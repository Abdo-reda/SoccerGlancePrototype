import time
import os
import logging
from datetime import datetime
from parameters import *
from build_models.inference import invokeInference, buildModel
from feature_extraction.feature_extractor import invokeExtraction
from feature_extraction.ConvertHQtoLQ import convert_video


def main(args):

    # ------ Setup of Logging & Time Stuff
    print(":)")
    start = time.time()

    # 1---- Convert from a HQ resolution to LQ ... is this needed ? ...
    '''
    logging.info('-----------------Start Step1: Extracting Features .......')
    convert_video(args, "tests/HQ_Test.mp4", "tests/LQ_Test.mp4")
    step1 = time.time()
    logging.info(f'-----------------Time for Step1: {step1 - start} seconds')
    '''
    # 2------- Build Model
    model = buildModel(
        weights=args.load_weights,
        input_size=args.feature_dim,
        num_classes=args.num_classes,
        window_size=args.window_size,
        vocab_size=args.vocab_size,
        framerate=int(args.framerate),
        pool=args.pool,
        model_name=args.model_name
    )

    # 3------- Extract features
    logging.info('-----------------Start Step2: Extracting Features .......')
    invokeExtraction(
        features_type=args.features_type,
        back_end=args.back_end,
        transform=args.transform,
        grabber=args.grabber,
        FPS=args.framerate,
        path_video_input=args.path_video,
        path_features_output=args.path_output,
        start=args.start,
        duration=args.duration,
        overwrite=args.overwrite,
    )
    step2 = time.time()
    logging.info(f'-----------------Time for Step2: {step2 - start} seconds')

    # 4------ Run Model on the extracted Features
    logging.info(
        '------------------Start Step3: Running Model & Getting output ........')
    invokeInference(
        model=model,
        input_features=args.input_features,
        window_size_frame=args.window_size_frame,
        framerate=int(args.framerate),
        num_classes=args.num_classes,
        NMS_window=args.NMS_window,
        NMS_threshold=args.NMS_threshold,
        version=args.version,
        model_name=args.model_name,
        output_folder=args.output_folder
    )
    step3 = time.time()
    logging.info(f'-----------------Time for Step3: {step3 - step2} seconds')

    logging.info(
        f'<-------------------------Total Time: {time.time() - start} seconds------------------->')


if __name__ == "__main__":

    # ----Get Any Parameters Regarding the Input Video & Model
    args = getParameters()
    manualArg = False
    if manualArg:
        args = setManualParameters(args)

    # ------Setup Logging, directory and level.
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    os.makedirs(os.path.join("models", args.model_name), exist_ok=True)
    log_path = os.path.join("models", args.model_name,
                            datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'))

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])

    # ----I think this sets up the values for some environment variables, not sure if they are used but they could be important ..
    if args.GPU >= 0:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.GPU)

    main(args)
