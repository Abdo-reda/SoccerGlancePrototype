
import os
import logging

try:
    # pip install tensorflow (==2.3.0)
    from tensorflow.keras.models import Model
    from tensorflow.keras.applications.resnet import preprocess_input
    # from tensorflow.keras.preprocessing.image import img_to_array
    # from tensorflow.keras.preprocessing.image import load_img
    from tensorflow import keras
except:
    print("issue loading TF2")
    pass

import numpy as np
import cv2  # pip install opencv-python (==3.4.11.41)
import imutils  # pip install imutils
import skvideo.io
from tqdm import tqdm
import pickle as pkl

from sklearn.decomposition import PCA, IncrementalPCA  # pip install scikit-learn
from sklearn.preprocessing import StandardScaler
import json

import random
from SoccerNet.utils import getListGames
from SoccerNet.Downloader import SoccerNetDownloader
from SoccerNet.DataLoader import Frame, FrameCV


class VideoFeatureExtractor():
    def __init__(self,
                 features_type="ResNET",
                 back_end="TF2",
                 overwrite=False,
                 transform="crop",
                 grabber="opencv",
                 FPS=2.0,
                 split="all"):

        self.features_type = features_type
        self.back_end = back_end
        self.verbose = True
        self.transform = transform
        self.overwrite = overwrite
        self.grabber = grabber
        self.FPS = FPS
        self.split = split

        if "TF2" in self.back_end:
            # create pretrained encoder (here ResNet152, pre-trained on ImageNet)
            base_model = keras.applications.resnet.ResNet152(include_top=True,
                                                             weights='imagenet',
                                                             input_tensor=None,
                                                             input_shape=None,
                                                             pooling=None,
                                                             classes=1000)

            # define model with output after polling layer (dim=2048)
            self.model = Model(base_model.input,
                               outputs=[base_model.get_layer("avg_pool").output])  # functional api not sequential, so we don't have to specify the input dimensions ...
            self.model.trainable = False

    def extractFeatures(self, path_video_input, path_features_output, start=None, duration=None, overwrite=False):
        logging.info(f"extracting features for video {path_video_input}")

        if os.path.exists(path_features_output) and not overwrite:
            logging.info(
                "Features already exists, use overwrite=True to overwrite them. Exiting.")
            return
        if "TF2" in self.back_end:

            if self.grabber == "skvideo":
                videoLoader = Frame(
                    path_video_input, FPS=self.FPS, transform=self.transform, start=start, duration=duration)
            elif self.grabber == "opencv":
                videoLoader = FrameCV(
                    path_video_input, FPS=self.FPS, transform=self.transform, start=start, duration=duration)

            frames = preprocess_input(videoLoader.frames)

            if duration is None:
                duration = videoLoader.time_second

            logging.info(
                f"frames {frames.shape}, fps={frames.shape[0]/duration}")

            # predict the features from the frames (adjust batch size for smaller GPU)
            features = self.model.predict(frames, batch_size=64, verbose=1)

            logging.info(
                f"features {features.shape}, fps={features.shape[0]/duration}")

        # save the featrue in .npy format
        os.makedirs(os.path.dirname(path_features_output), exist_ok=True)
        np.save(path_features_output, features)


class PCAReducer():
    def __init__(self, pca_file=None, scaler_file=None):
        self.pca_file = pca_file
        self.scaler_file = scaler_file
        self.loadPCA()

    def loadPCA(self):
        # Read pre-computed PCA
        self.pca = None
        if self.pca_file is not None:
            with open(self.pca_file, "rb") as fobj:
                self.pca = pkl.load(fobj)

        # Read pre-computed average
        self.average = None
        if self.scaler_file is not None:
            with open(self.scaler_file, "rb") as fobj:
                self.average = pkl.load(fobj)

    def reduceFeatures(self, input_features, output_features, overwrite=False):
        logging.info(f"reducing features {input_features}")

        if os.path.exists(output_features) and not overwrite:
            logging.info(
                "Features already exists, use overwrite=True to overwrite them. Exiting.")
            return
        feat = np.load(input_features)
        if self.average is not None:
            feat = feat - self.average
        if self.pca is not None:
            feat = self.pca.transform(feat)
        np.save(output_features, feat)


class GeneralFeatureExtractor:
    def __init__(self, feature_configuration=None):
        self.feature_configuration = feature_configuration
        self.feature_extractor = self.build_feature_extractor(
            self.feature_configuration)
        self.feature_reducer = self.build_feature_reducer(
            self.feature_configuration)

    def build_feature_extractor(self, feature_configuration):
        return VideoFeatureExtractor(
            overwrite=feature_configuration['overwrite'],
            features_type=feature_configuration['features_type'],
            back_end=feature_configuration['back_end'],
            transform=feature_configuration['transform'],
            grabber=feature_configuration['grabber'],
            FPS=feature_configuration['framerate']
        )

    def build_feature_reducer(self, feature_configuration):
        if feature_configuration['feature_reducer_type'] == 'PCA':
            return PCAReducer(feature_configuration['feature_reducer_path'], None)
        elif feature_configuration['feature_reducer_type'] == 'PCA_Scalar':
            return PCAReducer(None, feature_configuration['feature_reducer_path'])
        else:
            return None


def buildFeatureExtractor(feature_configuration):
    logging.info('Creating Feature Extractor with the following configuration:')
    logging.info(feature_configuration)
    return GeneralFeatureExtractor(feature_configuration)


def invokeExtraction(
    myFeatureExtractor,
    myPCAReducer,
    path_video_input,
    path_features_output,
    start,
    duration,
    overwrite,
):
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
