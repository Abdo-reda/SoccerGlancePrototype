import whisper
import time
import os

cwd = os.getcwd().split('\\')[-1]
if cwd != 'scripts':
    print('Please CD into the scripts folder and rerun the transcribe_audio.py script.')
    exit()

files = os.listdir('..\\generated_chunks\\audio_chunks')
print(files)
allFiles = []  #check for a new audio file

print('Waiting for audio files...')
label = False
counter=1
while True:
    files = os.listdir('..\\generated_chunks\\audio_chunks')

    # add all new files and endswith .mp3
    added = [f for f in files if f not in allFiles and f.endswith('.mp3')]

    # update allFiles with only the files that end with .mp3
    allFiles = [f for f in files if f.endswith('.mp3')]


    if not added:
        if label:
            print('Waiting for audio files...')
        label = False
        time.sleep(1)
    else:
        label = True
        for file in added:
            if not os.path.exists('..\\generated_chunks\\transcript_chunks'): #create directory for transcript_chunks if does not exist
                os.makedirs('..\\generated_chunks\\transcript_chunks')

            audio_file= file
            print('Audio file found: ' + audio_file)
            audio_path = '..\\generated_chunks\\audio_chunks\\' + audio_file
            model = whisper.load_model("base") # might change to another model for better accuracy
            time.sleep(3)
            result = model.transcribe(audio_path, fp16=False, language='English') #transcribe audio and save to result
            if counter < 10:
                file= open("..\\generated_chunks\\transcript_chunks\\transcript_chunk0" + str(counter) + ".txt", "w")
            else:
                file= open("..\\generated_chunks\\transcript_chunks\\transcript_chunk" + str(counter) + ".txt", "w")
            file.write(result["text"])  #create a text file for each transcription and save in transcript_chunks folder
            file.close()
            counter+=1
            os.remove(audio_path) #delete audio file after transcription