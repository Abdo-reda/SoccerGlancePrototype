import os
import logging
from VideoFeatureExtractor import buildFeatureExtractor, buildPCAReducer


def process_input(video_path):
    while True:
        files = os.listdir(video_path)
        added = [file for file in files if file.endswith('.mp4')]
        for file in added:
            generate_features(file)
            os.remove(file)


def generate_features(dir_path, input_path, video, audio, chunk_size, fps, counter):
    # logging.info('--------------Extracting Features .......')
    # extract features ...
    myFeatureExtractor.extractFeatures(path_video_input,
                                       path_features_output,
                                       start,
                                       duration,
                                       overwrite)

    # reduce features ...
    if myPCAReducer:
        myPCAReducer.reduceFeatures(input_features=path_features_output,
                                    output_features=path_features_output,
                                    overwrite=overwrite)
    # step2 = time.time()
    # logging.info(f'-----------------Time for Step2: {step2 - start} seconds')


def main(args):
    # ---- Build Feature Extractor -----
    feature_extractor = buildFeatureExtractor(
        features_type=args.features_type,
        back_end=args.back_end,
        transform=args.transform,
        grabber=args.grabber,
        FPS=args.framerate,
    )
    # ---- Build PCA Reducer ----
    pca_reducer = buildPCAReducer(
        pca_file=args.PCA,
        scaler_file=args.PCA_scaler
    )
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # process_input(dir_path)
    return


if __name__ == "__main__":
    # get arguments somehow....
    main()

    # /home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/chunk_generator/generated_chunks/video_chunks
