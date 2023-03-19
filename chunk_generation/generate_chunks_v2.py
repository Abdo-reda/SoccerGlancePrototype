from moviepy.editor import *
import os
import time
import cv2

source = "rtmp://localhost:1935/live/mystream"

def generate_chunks(dir_path, stream):
    frame_count = 0
    fps = stream.get(cv2.CAP_PROP_FPS) # 25 # get the frames per second of the stream
    chunk_size = int(fps * 5)  # set the chunk size to 5 seconds worth of frames
    frame_list = []
    chunk_num = 0

    while True:
        ret, frame = stream.read()

        # if frame is read successfully
        if ret:
            # append the frame to the frame list
            frame_list.append(frame)
            frame_count += 1

            # if we have enough frames for a chunk
            if frame_count >= chunk_size:
                # concatenate the frames and save as a video file
                filename = f'chunk{chunk_num}.mp4'
                out = cv2.VideoWriter(f"/home/g05-f22/Desktop/ActionSpotting/MyPrototype/SoccerNetPrototype/chunk_generation/generated_chunks/video_chunks/{filename}", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame.shape[1], frame.shape[0]))
                for frame in frame_list:
                    out.write(frame)
                out.release()

                # reset the variables
                chunk_num +=1
                frame_count = 0
                frame_list = []

        # ret, frame = stream.read()  # read the next frame from the stream
        # if not ret:
        #     break  # exit the loop if there are no more frames
    
        # if frame_count % chunk_size == 0:
        #     # if we've reached the end of a chunk, save the frames to a file
        #     filename = f'chunk{frame_count//chunk_size}.mp4'  # create a filename for the chunk
        #     writer = cv2.VideoWriter(dir_path + '/generated_chunks/video_chunks/video_chunk/' + filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame.shape[1], frame.shape[0]))  # create a writer to save the frames as a video file
        
        # writer.write(frame)  # write the first frame to the file

        # if frame_count % chunk_size == chunk_size - 1:
        #     writer.release()
        
        # frame_count += 1



def initialize():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    stream = cv2.VideoCapture(source)
    generate_chunks(dir_path, stream)

if __name__ == "__main__":
    initialize()


