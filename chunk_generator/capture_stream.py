import cv2
from datetime import datetime, timedelta, timezone
import urllib
import m3u8
import streamlink
import time
import os
import subprocess

def get_stream(url):
    tries = 10
    for i in range(tries):
        try:
            streams = streamlink.streams(url)
        except:
            if i < tries - 1:
                print(f"Attempt {i+1} of {tries}")
                time.sleep(0.1)
                continue
            else:
                raise
        break

    stream_url = streams["best"]
    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0] 


def dl_stream(url, filename):
    """
    Download each chunk to file
    input: url, filename
    output: saves file at filename location
    returns none.
    """
    pre_time_stamp = datetime(1, 1, 1, 0, 0, tzinfo=timezone.utc)

    newFileName = filename.split('.ts')[0]  + '01.ts'

    i=1
    while True:
        #Open stream
        stream_segment = get_stream(url)
    
        #Get current time on video
        cur_time_stamp = stream_segment.program_date_time
        #Only get next time step, wait if it's not new yet
        if cur_time_stamp <= pre_time_stamp:
            #Don't increment counter until we have a new chunk
            time.sleep(0.5) #Wait half a sec
            pass
        else:
            #Open file for writing stream
            file = open(newFileName, 'ab+') #ab+ means keep adding to file
            #Write stream to file
            with urllib.request.urlopen(stream_segment.uri) as response:
                html = response.read()
                file.write(html)
            
            #Update time stamp
            pre_time_stamp = cur_time_stamp
            time.sleep(stream_segment.duration) #Wait duration time - 1

            tsToMp4(newFileName, i)
            file.close()
            os.remove(newFileName)
        
            i += 1 #only increment if we got a new chunk
            if i < 10:
                newFileName = filename.split('.ts')[0]  + '0' + str(i) + '.ts'
            else:
                newFileName = filename.split('.ts')[0]  + str(i) + '.ts'
            
    return None

def tsToMp4(saved_video_file, idx):
    if not os.path.exists(dir_path + '/input_stream'):
        os.makedirs(dir_path + '/input_stream')
    
    if idx < 10:
        output_file = dir_path + '/input_stream/input_chunk0' + str(idx) + '.mp4'
    else:
        output_file = dir_path + '/input_stream/input_chunk' + str(idx) + '.mp4'

    print(saved_video_file, output_file)
    subprocess.run('ffmpeg -i ' + saved_video_file + ' ' + output_file, shell=True)

       
dir_path = os.path.dirname(os.path.realpath(__file__))
tempFile = dir_path + '/temp/temp.ts'  #files are format ts, open cv can view them
videoURL = 'https://www.youtube.com/watch?v=jDpVRarF9UM&ab_channel=WhiskeyBluesLounge' # test stream
dl_stream(videoURL, tempFile)