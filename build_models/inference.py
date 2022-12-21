import numpy as np
from .model import Model
import logging
import os
import torch
from SoccerNet.Evaluation.utils import AverageMeter, EVENT_DICTIONARY_V2, INVERSE_EVENT_DICTIONARY_V2
from SoccerNet.Evaluation.utils import EVENT_DICTIONARY_V1, INVERSE_EVENT_DICTIONARY_V1
import json


def feats2clip(feats, stride, clip_length, padding = "replicate_last", off=0):
    if padding =="zeropad":
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

    if padding=="replicate_last":
        idx = idx.clamp(0, feats.shape[0]-1)
    # print(idx)
    return feats[idx,...] #now its divided int windows with apt padding...

    

def invokeInference(args):

    '''

        TODO:
            * Seperate the directory of the test and file name, actually just assume we have a default directory for our tests maybe and you just want a name ...
            * fix everything !
    
    '''
 

    #--------------Set up some used variables (temporary)
    tempNumClasses = 17
    file_inference_features = '/home/g05-f22/Desktop/ActionSpotting/Prototype/tests/HQ_Test.npy'
    output_folder = '/home/g05-f22/Desktop/ActionSpotting/Prototype/tests/'
    window_size_frame = args.window_size*int(args.framerate)
    #test_id = '0'
   

    #-------------------- create/builds model
    model = Model(weights=args.load_weights, input_size=args.feature_dim,
                  num_classes=tempNumClasses, window_size=args.window_size, 
                  vocab_size = args.vocab_size,
                  framerate=int(args.framerate), pool=args.pool).cuda()
    
    logging.info(model)


    #--------------Loads the model // For the best model only
    checkpoint = torch.load(os.path.join("models", args.model_name, "model.pth.tar"))
    model.load_state_dict(checkpoint['state_dict'])


    #----------------------------Inference time

    #------Adjust the features/input to the model
    inference_features = np.load(file_inference_features)
    inference_features = inference_features.reshape(-1, inference_features.shape[-1]) #invert ..
    inference_features = feats2clip(torch.from_numpy(inference_features), stride=1, off=int(window_size_frame/2), clip_length=window_size_frame)
    inference_features = inference_features.squeeze(0) #removes a dimension for some reason ... 

    #------I think we divide the input into chunks ...
    BS = 256 #512 ... for two frames ... if each frame results in 256 features ... 
    timestamp_inference = []
    for b in range(int(np.ceil(len(inference_features)/BS))): #loop over frames? so handle the feature of each frame.
        start_frame = BS*b
        end_frame = BS*(b+1) if BS * \
            (b+1) < len(inference_features) else len(inference_features)
        feat = inference_features[start_frame:end_frame].cuda()
        output = model(feat).cpu().detach().numpy() 
        timestamp_inference.append(output)


    #------
    timestamp_inference = np.concatenate(timestamp_inference) #takes a list of arrays and concatonates them in to a single axis Default is 0.
    timestamp_inference = timestamp_inference[:, 1:] #this slices the array I think, it returns 1: ?????!!!!!! takes everything from first dimension and everyhing from second dimension starting from column 1. //every row and every column except the first column .... 
    
    def get_spot_from_NMS(Input, window=60, thresh=0.0):

        detections_tmp = np.copy(Input)
        indexes = []
        MaxValues = []

        while(np.max(detections_tmp) >= thresh):

            # Get the max remaining index and value
            max_value = np.max(detections_tmp)
            max_index = np.argmax(detections_tmp)
            MaxValues.append(max_value)
            indexes.append(max_index)

            # detections_NMS[max_index,i] = max_val
            nms_from = int(np.maximum(-(window/2)+max_index,0))
            nms_to = int(np.minimum(max_index+int(window/2), len(detections_tmp)))
            detections_tmp[nms_from:nms_to] = -1

        return np.transpose([indexes, MaxValues])

    framerate = int(args.framerate)
    get_spot = get_spot_from_NMS

    json_data = dict()
    json_data["UrlLocal"] = 0
    json_data["predictions"] = list()

    for half, timestamp in enumerate([timestamp_inference]):
        for l in range(tempNumClasses):
            spots = get_spot(
                timestamp[:, l], window=args.NMS_window*framerate, thresh=args.NMS_threshold)
            for spot in spots:
                # print("spot", int(spot[0]), spot[1], spot)
                frame_index = int(spot[0])
                confidence = spot[1]
                # confidence = predictions_half_1[frame_index, 
                seconds = int((frame_index//framerate)%60)
                minutes = int((frame_index//framerate)//60)
                prediction_data = dict()
                prediction_data["gameTime"] = str(half+1) + " - " + str(minutes) + ":" + str(seconds)
                if args.version== 2:
                    prediction_data["label"] = INVERSE_EVENT_DICTIONARY_V2[l]
                else:
                    prediction_data["label"] = INVERSE_EVENT_DICTIONARY_V1[l]
                prediction_data["position"] = str(int((frame_index/framerate)*1000))
                prediction_data["half"] = str(half+1)
                prediction_data["confidence"] = str(confidence)
                json_data["predictions"].append(prediction_data)
                
    os.makedirs(os.path.join("models", args.model_name, output_folder), exist_ok=True)
    with open(os.path.join("models", args.model_name, output_folder, "results_spotting.json"), 'w') as output_file:
        json.dump(json_data, output_file, indent=4)


   
    return 
