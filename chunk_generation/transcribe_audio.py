import whisper
import time
import os
import sys
import psutil

MODEL_TYPE = "medium"

def process_input(pid):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    allFiles = []  #check for a new audio file
    print('Waiting for audio files...')
    label = False
    CHUNK_NUM=0
    process_handle = psutil.Process(pid)
    
    while True:
        files = os.listdir(dir_path + '/generated_chunks/audio_chunks')

        # add all new files and endswith .wav
        added = [f for f in files if f not in allFiles and f.endswith('.wav')]
        # update allFiles with only the files that end with .wav
        allFiles = [f for f in files if f.endswith('.wav')]
      

        if not added:
            if label:
                print('Waiting for audio files...')
            label = False
            time.sleep(1)
        else:
            
            label = True
            for file in added:
                
                is_file_use = True
                audio_file= file
                print('Audio file found: ' + audio_file)
                audio_path = dir_path + '/generated_chunks/audio_chunks/' + audio_file
                
                while is_file_use:
                    # print("Audio Path: ", audio_path)
                    # print("Open File: ", open_file )
                        
                    file_handles = process_handle.open_files()
                    for fh in file_handles:
                        if(audio_path == fh.path):
                            is_file_use = True 
                            break
                        is_file_use = False

                    pass
                
                model = whisper.load_model(MODEL_TYPE) # might change to another model for better accuracy
                time.sleep(1)
                result = model.transcribe(audio_path, fp16=False) #transcribe audio and save to result
                if CHUNK_NUM < 10:
                    file= open(dir_path + '/generated_chunks/transcript_chunks/transcript_chunk0' + str(CHUNK_NUM) + '.txt', 'w')
                else:
                    file= open(dir_path + '/generated_chunks/transcript_chunks/transcript_chunk' + str(CHUNK_NUM) + '.txt', 'w')
                file.write(result["text"])  #create a text file for each transcription and save in transcript_chunks folder
                file.close()
                CHUNK_NUM+=1
                # os.remove(audio_path) #delete audio file after transcription

def initialize():
    pid = int(sys.argv[1])
    process_input(pid)

if __name__ == "__main__":
    initialize()