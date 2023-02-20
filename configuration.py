import yaml


class Configuration:
    def __init__(
            self,
            configuration_file='/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/configuration.yaml'
    ):
        self.configuration_file = configuration_file

    def get_default_configuration(self):
        framerate = 1.0
        window_size = 15
        num_classes = 17
        model_name = 'NetVLAD'
        data = {
            'model_configuration': {
                'weights': None,
                'feature_dim': 512,  # input_size
                'num_classes': num_classes,
                'window_size': window_size,  # chunk_size in sec
                'vocab_size': 64,
                'framerate': int(framerate),  # needs to be int
                'pool': 'NetVLAD++',
                'model_name': model_name,   # needs to match the model file name
            },
            'feature_configuration': {
                'features_type': 'BAIDU',   #
                'input_path': '/chunk_generator/generated_chunks/video_chunks/',
                'output_path': '/generated_features/',
                'overwrite': True,
                'video_res': 'LQ',
                'back_end': 'TF2',
                'transform': 'crop',
                'grabber': 'opencv',
                'framerate': framerate,  # needs to be float
                'reduce_feature_type': 'PCA',
                'feature_reducer': 'pca_512_TF2.pkl',
            },
            'inference_configuration': {
                'input_path': '/generated_features/',
                'output_path': '/generated_output/' + model_name,
                'window_size_frame': window_size * int(framerate),
                'framerate': framerate,
                'num_classes': num_classes,
                'NMS_window': 30,
                'NMS_threshold': 0.0,
                'version': 2,
            }
        }
        return data

    def save_configuration(self):
        data = self.get_default_configuration()
        with open(self.configuration_file, 'w') as f:
            yaml.dump(data, f)

    def update_configuration(self):
        data = self.get_default_configuration()
        yaml.dump(data, self.configuration_file)

    def get_configuration(self):
        return yaml.load(self.configuration_file)

    def validate_configuration(data):
        # this function will later be used to validate the data returned from the get_configuration ...
        return True


''' 
    Description of the different parameters, default values, so on .. should be here
        - 'features_type', type=str, default="ResNET", help="ResNET or R25D [default:ResNET]"
        - 'back_end', type=str, default="TF2", help="Backend TF2 or PT [default:TF2]"
        - 'PCA', type=str, default="pca_512_TF2.pkl", help="Pickle with pre-computed PCA"
        - 'PCA_scaler', type=str, default="average_512_TF2.pkl", help="Pickle with pre-computed PCA scaler"
        - 'feature_dim', required=False, type=int, default=None,     help='Number of input features'
        - 'framerate', type=float, default=2.0, help="FPS for the features [default:2.0]"

'''

if __name__ == "__main__":
    myConfiguration = Configuration()
    myConfiguration.save_configuration()
