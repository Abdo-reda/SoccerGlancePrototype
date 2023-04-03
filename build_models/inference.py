import numpy as np
from .model import Model
import logging
import os
import torch
from SoccerNet.Evaluation.utils import AverageMeter, EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V1, INVERSE_EVENT_DICTIONARY_V1
import json
import datetime
import requests


def feats2clip(feats, stride, clip_length, padding="replicate_last", off=0):
    if padding == "zeropad":
        print("beforepadding", feats.shape)
        pad = feats.shape[0] - int(feats.shape[0]/stride)*stride
        print("pad need to be", clip_length-pad)
        m = torch.nn.ZeroPad2d((0, 0, clip_length-pad, 0))
        feats = m(feats)
        print("afterpadding", feats.shape)
        # nn.ZeroPad2d(2)

    idx = torch.arange(start=0, end=feats.shape[0]-1, step=stride)
    idxs = []
    for i in torch.arange(-off, clip_length-off):
        idxs.append(idx+i)
    idx = torch.stack(idxs, dim=1)

    if padding == "replicate_last":
        idx = idx.clamp(0, feats.shape[0]-1)
    # print(idx)
    return feats[idx, ...]  # now its divided int windows with apt padding...


def buildModel(model_configuration):
    # -------------------- create/builds model
    model = Model(
        weights=model_configuration['weights'],
        input_size=model_configuration['feature_dim'],
        num_classes=model_configuration['num_classes'],
        window_size=model_configuration['window_size'],
        vocab_size=model_configuration['vocab_size'],
        framerate=model_configuration['framerate'],
        pool=model_configuration['pool']
    ).cuda()

    logging.info(model)

    # --------------Loads the model // For the best model only
    checkpoint = torch.load(os.path.join(
        "/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/build_models/models", model_configuration['model_name'], "model.pth.tar")) 
    model.load_state_dict(checkpoint['state_dict'])

    return model


def invokeInference(
        model,
        input_features,
        window_size_frame,
        framerate,
        num_classes,
        NMS_window,
        NMS_threshold,
        version,
        output_folder,
        chunk_num,
        chunk_size, 
        ):
    '''
        TODO:
            * Seperate the directory of the test and file name, actually just assume we have a default directory for our tests maybe and you just want a name ...
            * fix everything !
    '''

    # ----------------------------Inference time

    # ------Adjust the features/input to the model
    inference_features = np.load(input_features)
    # invert ..
    inference_features = inference_features.reshape(
        -1, inference_features.shape[-1])
    inference_features = feats2clip(torch.from_numpy(inference_features), stride=1, off=int(
        window_size_frame/2), clip_length=window_size_frame)
    # removes a dimension for some reason ...
    inference_features = inference_features.squeeze(0)

    # ------I think we divide the input into chunks ...
    # 512 ... for two frames ... if each frame results in 256 features ...
    BS = 256
    timestamp_inference = []
    # loop over frames? so handle the feature of each frame.
    for b in range(int(np.ceil(len(inference_features)/BS))):
        start_frame = BS*b
        end_frame = BS*(b+1) if BS * \
            (b+1) < len(inference_features) else len(inference_features)
        feat = inference_features[start_frame:end_frame].cuda()
        output = model(feat).cpu().detach().numpy()
        timestamp_inference.append(output)

    # ------
    # takes a list of arrays and concatonates them in to a single axis Default is 0.
    timestamp_inference = np.concatenate(timestamp_inference)
    # this slices the array I think, it returns 1: ?????!!!!!! takes everything from first dimension and everyhing from second dimension starting from column 1. //every row and every column except the first column ....
    timestamp_inference = timestamp_inference[:, 1:]

    def get_spot_from_NMS(Input, window=60, thresh=0.0):

        detections_tmp = np.copy(Input)
        indexes = []
        MaxValues = []

        while (np.max(detections_tmp) >= thresh):

            # Get the max remaining index and value
            max_value = np.max(detections_tmp)
            max_index = np.argmax(detections_tmp)
            MaxValues.append(max_value)
            indexes.append(max_index)

            # detections_NMS[max_index,i] = max_val
            nms_from = int(np.maximum(-(window/2)+max_index, 0))
            nms_to = int(np.minimum(
                max_index+int(window/2), len(detections_tmp)))
            detections_tmp[nms_from:nms_to] = -1

        return np.transpose([indexes, MaxValues])

    get_spot = get_spot_from_NMS
    json_data = dict()
    json_data["UrlLocal"] = 0
    json_data["predictions"] = list()

    for half, timestamp in enumerate([timestamp_inference]):
        for l in range(num_classes):
            spots = get_spot(
                timestamp[:, l], window=NMS_window*framerate, thresh=NMS_threshold)
            for spot in spots:
                # print("spot", int(spot[0]), spot[1], spot)
                frame_index = int(spot[0])
                confidence = spot[1]
                # confidence = predictions_half_1[frame_index,
                seconds = int((frame_index//framerate) % 60) + chunk_num*chunk_size
                minutes = int(seconds/60) # seconds = int((frame_index//framerate) % 60)
                seconds = seconds % 60
                prediction_data = dict()
                prediction_data["gameTime"] = str(
                    half+1) + " - " + str(datetime.timedelta(seconds=seconds))
                if version == 2:
                    prediction_data["label"] = INVERSE_EVENT_DICTIONARY_V2[l]
                else:
                    prediction_data["label"] = INVERSE_EVENT_DICTIONARY_V1[l]
                prediction_data["position"] = str(
                    int((frame_index/framerate)*1000))
                prediction_data["half"] = str(half+1)
                prediction_data["confidence"] = str(confidence)
                json_data["predictions"].append(prediction_data)

    #------------------------- send
  
    for x in json_data['predictions']:
        json_obj = json.dumps(x)
        headers = {'Content-type': 'application/json'}
        requests.post('http://localhost:5000/recieve_action', data=json_obj, headers=headers)
    

    with open(os.path.join(output_folder, "results_spotting.json"), 'a+') as output_file:
        output_file.write(f'\n//---------------------------- NEW CHUNK {chunk_num} ------------------------------\n')
        json.dump(json_data, output_file, indent=4)
        

    return

def generateOutput(model, inference_configuration, chunk_num, chunk_size):
    invokeInference(
        model=model, 
        input_features=inference_configuration['input_path'],
        window_size_frame=inference_configuration['window_size_frame'],
        framerate=inference_configuration['framerate'],
        num_classes=inference_configuration['num_classes'],
        NMS_window=inference_configuration['NMS_window'],
        NMS_threshold=inference_configuration['NMS_threshold'],
        version=inference_configuration['version'],
        output_folder=inference_configuration['output_path'],
        chunk_num = chunk_num,
        chunk_size = chunk_size,
    )
