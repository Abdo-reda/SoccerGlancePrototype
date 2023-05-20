

### Setup Enviornment 
* conda create -y -n PrototypeEnv python=3.9
* conda activate PrototypeEnv
* conda install -y cudnn=8.2
* conda install -y cudatoolkit=11.3
* conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
* pip3 install -r requirements.txt

-------------- 
### Notes & Prerequistes

* This project mainly depends that an <b> nginx server with an rtmp module </b> is already setup to accept streams on rtmp://localhost:1935/live/ 
    * However the code could be modified to accept streams from whenever, the SOURCE will just need to be modified in the server.py file.
    * Morover, The nginx.config that was used is included in the project directory for reference.

--------------
### Using the Prototype

* To activate the enviornment 
    * `conda activate PrototypeEnv`
* To run the model server 
    * `python server/server.py`
    * You can then open http://localhost:5000/ and click on process stream button to start generating processing the video stream (this will simply execute the main.py script)   
* To run an example of a client server 
    * `python client_server/client_server.py`

--------------
### Project Structure

* <b> Main Directory </b>
    * `main.py` this is the main script that is responsible for creating and executing other python scripts/processes that will process the video stream.
    * `configuration.py` is responsible for setting up parameters (a yaml file) that was used in the action spotting model (creating the features and generating actions).
    * `offline_prototype.py` this is the old script that generates actions for a downloaded video.
* <b> Server Directory </b> Contains the main logic for the model server.
    * `server.py` this is the main model server, it processes the video streams and communicates with the api.
    * `api_service.py` this is a script that contains the most common calls/functions to the api, for example sending highlights or match is live and so on ..
* <b> Client Server Directory </b>
    * `client_server.py` this an example for what a client application would look like, this was created to test that the clients can recieve the highlights.
* <b> Chunk_Generation </b>
    * `transcribe_audio.py` this script is reponsible for transcribing the audio chunks.
    * `extract_highlights.py`this script is reponsible for generating highlights from the transcribed audio chunks.
    * `extract_actions.py` this script is responsbile for generating actions from the transcriptions.
    * `capture_stream.py` this script was used to capture a video stream from interent/youtube using streamlink and store that data in temp folder.
    * `generate_chunks.py` this script was used to generate video chunks from the data that was caputred by capture_stream.py.
* <b> Build_Models [Archived] </b>
    * This contains different scripts that will reponsible for training and creating an instance of the model that was used for action spotting.
* <b> Feature_Generation [Archived] </b>
    * `generate_features.py` this script is reponsbile for extracting features which will later be used to extract actions from the video stream.
* <b> Output_Generation [Archived] </b>
    * `generate_output.py` this script is reponsible for generating actions from the extracted features from the video.

