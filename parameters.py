import argparse
#import os


def getParameters():
    parser = argparse.ArgumentParser(
        description='Video Parameters', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # ------ Common Parameters (Features)
    parser.add_argument('--features', type=str, default="ResNET", help="ResNET or R25D [default:ResNET]")
    parser.add_argument('--back_end', type=str, default="TF2", help="Backend TF2 or PT [default:TF2]")
    parser.add_argument('--PCA', type=str, default="pca_512_TF2.pkl", help="Pickle with pre-computed PCA")
    parser.add_argument('--PCA_scaler', type=str, default="average_512_TF2.pkl", help="Pickle with pre-computed PCA scaler")
    parser.add_argument('--feature_dim', required=False, type=int,   default=None,     help='Number of input features' )
        #shouldn't the feature_dim be a result of the above choices ..., so this used for the model I think ..? 
    parser.add_argument('--framerate', type=float, default=2.0, help="FPS for the features [default:2.0]")
        #  parser.add_argument('--features',   required=False, type=str,   default="ResNET_TF2.npy",     help='Video features' )
    parser.add_argument('--GPU', required=False, type=int, default=0, help='ID of the GPU to use' )
    parser.add_argument('--loglevel', required=False, type=str, default='INFO', help='logging level')
        # parser.add_argument('--logging_dir',       required=False, type=str,   default="log", help='Where to log' )


    # ----- video setup
    parser.add_argument('--path_video', type=str, required=True, help="Path of the Input Video")
    parser.add_argument('--path_output', type=str, required=True, help="Path of the Output Features")
    parser.add_argument('--start', type=float, default=None, help="time of the video to strat extracting features [default:None]")
    parser.add_argument('--duration', type=float, default=None, help="duration of the video before finishing extracting features [default:None]")
    parser.add_argument('--overwrite', action="store_true", help="Overwrite the features.")
    parser.add_argument('--video_res', type=str, default="LQ", help="LQ or HQ? [default:LQ]")
    parser.add_argument('--transform', type=str, default="crop", help="crop or resize? [default:crop]")
    parser.add_argument('--grabber', type=str, default="opencv", help="skvideo or opencv? [default:opencv]")

    # ----- model setup
 
    # inference parameters
    parser.add_argument('--model_name', required=False, type=str, default="NetVLAD++",  help='named of the model to save' )

    # testing/evaulation parameters
    parser.add_argument('--SoccerNet_path', required=False, type=str,   default="/path/to/SoccerNet/", help='Path for SoccerNet' )
    parser.add_argument('--test_only', required=False, action='store_true',  help='Perform testing only' )
    parser.add_argument('--version', required=False, type=int,   default=2,     help='Version of the dataset' )
    parser.add_argument('--split_test', nargs='+', default=["test", "challenge"], help='list of split for testing')
    parser.add_argument('--load_weights', required=False, type=str,   default=None,     help='weights to load' )


    # train parameters
    parser.add_argument('--max_epochs', required=False, type=int, default=1000,     help='Maximum number of epochs' )
    parser.add_argument('--evaluation_frequency', required=False, type=int,   default=10,     help='Number of chunks per epoch' )
    parser.add_argument('--batch_size', required=False, type=int, default=256,     help='Batch size' )
    parser.add_argument('--LR', required=False, type=float, default=1e-03, help='Learning Rate' )
    parser.add_argument('--LRe', required=False, type=float, default=1e-06, help='Learning Rate end' )
    parser.add_argument('--patience', required=False, type=int,   default=10,     help='Patience before reducing LR (ReduceLROnPlateau)' )
    parser.add_argument('--split_train', nargs='+', default=["train"], help='list of split for training')
    parser.add_argument('--split_valid', nargs='+', default=["valid"], help='list of split for validation')
    parser.add_argument('--window_size', required=False, type=int, default=15,     help='Size of the chunk (in seconds)' )
    parser.add_argument('--pool', required=False, type=str, default="NetVLAD++", help='How to pool' )
    parser.add_argument('--vocab_size', required=False, type=int, default=64, help='Size of the vocabulary for NetVLAD' )
    parser.add_argument('--NMS_window', required=False, type=int, default=30, help='NMS window in second' )
    parser.add_argument('--NMS_threshold', required=False, type=float, default=0.0, help='NMS threshold for positive results' )
    parser.add_argument('--max_num_worker',   required=False, type=int,   default=4, help='number of worker to load data')
    parser.add_argument('--seed',   required=False, type=int,   default=0, help='seed for reproducibility')


    args = parser.parse_args()

    #--------------Set up some used variables (temporary)
    args.num_classes = 17
    args.input_features = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/tests/HQ_Test.npy'
    args.output_folder = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/tests/tempResults/'
    args.window_size_frame = args.window_size*int(args.framerate)

    return args



def setManualParameters(args):
    
    # ------ 
    args.features
    args.back_end
    args.PCA
    args.PCA_scaler
    args.feature_dim
    args.framerate
    args.GPU
    args.loglevel
    args.path_video
    args.path_output
    args.start
    args.duration
    args.overwrite
    args.video_res
    args.transform
    args.grabber
    args.model_name
    args.SoccerNet_path
    args.test_only
    args.version
    args.split_test
    args.load_weights
    args.max_epochs
    args.evaluation_frequency  
    args.batch_size
    args.LR
    args.LRe
    args.patience
    args.split_train
    args.split_valid
    args.window_size
    args.pool
    args.vocab_size
    args.NMS_window
    args.NMS_threshold
    args.max_num_worker
    args.seed


    return args