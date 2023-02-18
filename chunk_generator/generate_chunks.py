from moviepy.editor import *
import os
import time

# function to generate the video and audio chunks
def generate_chunks(video, audio, chunk_size, fps, counter):
    length = video.duration # length in seconds
    rem = length % chunk_size
    rem = int(rem)
    if rem != 0:
        length = length - rem
    for i in range(0, int(length), chunk_size):
        counter += 1
        if counter < 10:
            counter = '0' + str(counter)

        video.subclip(i, i+chunk_size).write_videofile("../generated_chunks/video_chunks/video_chunk{}.mp4".format(counter),fps=fps)
        audio.subclip(i, i+chunk_size).write_audiofile("../generated_chunks/audio_chunks/audio_chunk{}.mp3".format(counter))
    if rem != 0:
        counter += 1
        if counter < 10:
            counter = '0' + str(counter)
        video.subclip(length, length+rem).write_videofile("../generated_chunks/video_chunks/video_chunk{}.mp4".format(counter),fps=fps)
        audio.subclip(length, length+rem).write_audiofile("../generated_chunks/audio_chunks/audio_chunk{}.mp3".format(counter))

    print('Chunks generated. Deleting ' + input_file + '...')
    os.remove(input_path) # delete the input file after generating the chunks




cwd = os.path.basename(os.getcwd())
if cwd != 'scripts':
    print('Please CD into the scripts folder and rerun the generate_chunks.py script.')
    exit()



# check if the input folder exists
if not os.path.exists('../input_stream'):
    print('Creating the input folder...')
    os.makedirs('../input_stream')





print('Waiting for input video files...')
label = False
while True:
    files = os.listdir('../input_stream')
    added = [file for file in files if file.endswith('.mp4')]
    
    if added:
        label = True
        for file in added:
            input_file = file
            print('Input file found: ' + input_file)
            # load the video and audio
            input_path = '../input_stream/' + input_file
            time.sleep(3) # wait for the file to be fully copied to the input folder
            video = VideoFileClip(input_path)
            audio = video.audio

            # create the output folders if they don't exist
            if not os.path.exists('../generated_chunks'):
                os.makedirs('../generated_chunks')
            if not os.path.exists('../generated_chunks/video_chunks'):
                os.makedirs('../generated_chunks/video_chunks')
            if not os.path.exists('../generated_chunks/audio_chunks'):
                os.makedirs('../generated_chunks/audio_chunks')



            # check if there are any chunks left from the previous run
            res = [file for file in os.listdir('../generated_chunks/video_chunks') if file.endswith('.mp4')]
            max_chunk = 0
            for file in res:
                chunk = int(file.split('video_chunk')[1].split('.mp4')[0])
                if chunk > max_chunk:
                    max_chunk = chunk

                
            if max_chunk > 0:
                # the model should delete the chunks after processing. If some chunks are left, append to the existing chunks.
                print('Some chunks are yet to be handled. Appending to the existing chunks.') 
                counter = max_chunk
            else:
                counter = 0
                
            # counter is the same for video and audio chunks since we want corresponding chunks to have a common name 
            # (e.g. video_chunk1.mp4 and audio_chunk1.mp3) so that they can be easily matched when comparing the outputted action

            # customize the chunk size and fps based on the model needs
            chunk_size = 5 # in seconds
            fps = video.fps # frames per second (could customize based on model needs)

            # generate the chunks
            print('Generating the chunks...')
            generate_chunks(video, audio, chunk_size, fps, counter)
           
    else:
        if label:
            print('Waiting for input video files...')
        label = False
        time.sleep(1)  