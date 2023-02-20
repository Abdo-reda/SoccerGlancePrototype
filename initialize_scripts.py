import os
import subprocess
import signal
import logging
import time
from datetime import datetime
from parameters import *
from build_models.inference import invokeInference, buildModel


def create_folders(dir_path):
    # create the output folders if they don't exist
    if not os.path.exists(dir_path + '/input_stream'):
        os.makedirs(dir_path + '/input_stream')
    if not os.path.exists(dir_path + '/generated_chunks'):
        os.makedirs(dir_path + '/generated_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/video_chunks'):
        os.makedirs(dir_path + '/generated_chunks/video_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/audio_chunks'):
        os.makedirs(dir_path + '/generated_chunks/audio_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/transcript_chunks'):
        os.makedirs(dir_path + '/generated_chunks/transcript_chunks')


PROCESSING = True


def main(args):
    # ---------------- Initialize some stuff
    # timer = time.time()
    # --- Build Model & ...
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


    # create_folders(dir_path) #is this really needed?

    # ---------------- Capture Stream and Generate Chunks
    dir_path = os.path.dirname(os.path.realpath(__file__))
    process_capture_stream = subprocess.Popen(
        ['python', dir_path + '/chunk_generator/capture_stream.py'])
    process_generate_chunks = subprocess.Popen(
        ['python', dir_path + '/chunk_generator/generate_chunks.py'])
    process_transcribe_audio = subprocess.Popen(
        ['python', dir_path + '/chunk_generator/transcribe_audio.py'])

    # --------------- Process Chunks and Generate Output

    # --------------- Handling Program Exit

    def handling_program_exit(signal_number, frame):
        process_capture_stream.terminate()
        process_generate_chunks.terminate()
        process_transcribe_audio.terminate()
        global PROCESSING
        PROCESSING = False
        print('\n-------exiting------\n')

    signal.signal(signal.SIGINT, handling_program_exit)
    while PROCESSING:
        # ....processing
        pass


if __name__ == "__main__":

    # -----Get Any Parameters Regarding the Input Video & Model
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

    # ----Sets up the values for some environment variables, not sure if they are used but they could be important ..
    if args.GPU >= 0:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.GPU)

    main(args)
