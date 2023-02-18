import os
import subprocess
import signal

def create_folders(dir_path):
     # create the output folders if they don't exist
    if not os.path.exists(dir_path + '/input_stream'):
        os.makedirs(dir_path + '/input_stream')
    if not os.path.exists(dir_path + '/generated_chunks'):
        os.makedirs(dir_path + '/generated_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/video_chunks'):
        os.makedirs(dir_path + '/generated_chunks/video_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/audio_chunks'):
        os.makedirs(dir_path + '/generated_chunks/audio_chunks')
    if not os.path.exists(dir_path + '/generated_chunks/transcript_chunks'): 
        os.makedirs(dir_path + '/generated_chunks/transcript_chunks')

PROCESSING = True

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    create_folders(dir_path)
    process_1 = subprocess.Popen(['python', dir_path + '/capture_stream.py'])
    process_2 = subprocess.Popen(['python', dir_path + '/generate_chunks.py'])
    process_3 = subprocess.Popen(['python', dir_path + '/transcribe_audio.py'])
    def handling_program_exit(signal_number,frame):
        process_1.terminate()
        process_2.terminate()
        process_3.terminate()
        global PROCESSING 
        PROCESSING = False
        print('\n-------exiting------\n')

    signal.signal(signal.SIGINT,handling_program_exit)
    while PROCESSING:
        #....processing
        pass




if __name__ == "__main__":
    main()






    

