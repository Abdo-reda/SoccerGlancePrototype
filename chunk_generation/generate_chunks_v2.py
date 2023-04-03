from moviepy.editor import *
import os
import time
import cv2
import subprocess

source = "rtmp://localhost:1935/live/mystream"
chunk_duration = 5
temp_output_path = '/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/chunk_generation/generated_chunks/audio_chunks'

def generate_chunks(dir_path, stream):
    frame_count = 0
    fps =  stream.get(cv2.CAP_PROP_FPS) # 25 # get the frames per second of the stream
    chunk_size = int(fps * chunk_duration)  # set the chunk size to chunk_duration seconds worth of frames
    frame_list = []
    chunk_num = 0


    while True:
        ret, frame = stream.read()
        if ret:
            frame_list.append(frame)
            frame_count += 1
            if frame_count >= chunk_size:
                filename = f'chunk{chunk_num}.mp4'
                out = cv2.VideoWriter(f"/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/chunk_generation/generated_chunks/video_chunks/{filename}", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame.shape[1], frame.shape[0]))
                for frame in frame_list:
                    out.write(frame)
                out.release()
                chunk_num +=1
                frame_count = 0
                frame_list = []



def initialize():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    stream = cv2.VideoCapture(source)
    generate_chunks(dir_path, stream)

if __name__ == "__main__":
    initialize()

#ffmpeg -i rtmp://localhost:1935/live/mystream -f segment -segment_time 30 -codec:a pcm_s16le -ar 44100 -ac 2 output_%03d.wav
#'ffmpeg -t ' + chunk_duration + ' -i ' + source +' -c copy /generated_chunks/audio_chunks/output.mp3'