import yaml
import os


class Configuration:
    def __init__(
            self,
            configuration_path='/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/configuration.yaml'
    ):
        self.configuration_path = configuration_path
        self.configuration_file = open(self.configuration_path, 'r+')
        self.configuration_file.seek(0)

    def get_default_configuration(self):
        default_path = os.path.dirname(os.path.realpath(__file__))
        framerate = 2.0
        window_size = 15
        num_classes = 17
        model_name = 'NetVLAD++'
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
                'input_path': default_path + '/chunk_generator/generated_chunks/video_chunks/',
                'output_path': default_path + '/feature_extraction/generated_features/',
                'overwrite': True,
                'video_res': 'LQ',
                'back_end': 'TF2',
                'transform': 'crop',
                'grabber': 'opencv',
                'framerate': framerate,  # needs to be float
                'feature_reducer_type': 'PCA',
                'feature_reducer_path': default_path + '/feature_extraction/pca_512_TF2.pkl',
            },
            'inference_configuration': {
                'input_path': default_path + '/feature_extraction/generated_features/',
                'output_path': default_path + '/output_generation/generated_output/',
                'window_size_frame': window_size * int(framerate),
                'framerate': framerate,
                'num_classes': num_classes,
                'NMS_window': 30,
                'NMS_threshold': 0.6,
                'version': 2,
            }
        }
        return data

    def save_configuration(self):
        data = self.get_default_configuration()
        yaml.dump(data, self.configuration_file)
        self.configuration_file.seek(0)

    def update_configuration(self):
        data = self.get_default_configuration()
        yaml.dump(data, self.configuration_file)

    def get_configuration(self):
        return yaml.safe_load(self.configuration_file)

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
    # print(myConfiguration.get_configuration())
    # print('-------------------------------------------------')
    # tempConfig = Configuration()
    # print(tempConfig.get_configuration())
