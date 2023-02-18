

### Setup Enviornment 
* conda create -y -n MyPrototype python=3.7
* conda activate MyPrototype
* conda install -y cudnn=8.2
* conda install -y cudatoolkit=11.3
* conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
* pip3 install -r requirements.txt

//Note: that -y makes every prompt yes

### New Environment
* conda create -y -n MyNewPrototype python=3.9
* conda activate MyNewPrototype
* conda install -y cudnn=8.2
* conda install -y cudatoolkit=11.3
* conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
* pip3 install -r requirements.txt


### Using the Prototype

`conda activate MyPrototype`

`python3 prototype.py --path_video "tests/HQ_Test.mp4" --path_output "tests/HQ_Test.npy" --video_res HQ --start 0 --duration 60 --overwrite --PCA "feature_extraction/pca_512_TF2.pkl" --PCA_scaler "feature_extraction/average_512_TF2.pkl" --model_name=NetVLAD++ --features=ResNET_TF2_PCA512.npy --feature_dim=512 --NMS_threshold=0.3`

`python3 prototype.py --path_video "tests/LQ_Test.mp4" --path_output "tests/LQ_Test.npy" --video_res LQ --start 0 --duration 60 --overwrite --PCA "feature_extraction/pca_512_TF2.pkl" --PCA_scaler "feature_extraction/average_512_TF2.pkl" --model_name=NetVLAD++ --features=ResNET_TF2_PCA512.npy --feature_dim=512 --NMS_threshold=0.3`

//Note: there is a difference in the name of the features for some reason that the model accepts

### Notes

- Made the import inside the directories relative by using . 
    //from .model import Model

- Upgraded Tensorflow version hopefully this works ... why the internet so slow ....  original ==2.3.0 
    https://www.tensorflow.org/install/pip

- The missing library (7) is fucking optional I think and is realted to tenosRT which is not needed right now ... 
    //the actual 

- Tensor RT is probably not needed ...

- PCI_ID 0000:02:00.0 ... I think

- Whisper requires python version 3.9, I am scared that if I change the python version then the whole prototype will collapse, could create another conda env just in case ...
    - for new version git+https://github.com/openai/whisper.git
    - for python=3.7 version openai-whisper==20230124