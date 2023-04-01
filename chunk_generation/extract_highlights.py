import openai
import time
import os
import json
import requests

openai.api_key = "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"
model_engine = "text-davinci-003"

dir_path = os.path.dirname(os.path.realpath(__file__))
allFiles = []  #check for a new audio file
label = False
CHUNK_NUM=0
CHUNK_DUR=30

team1 = "Barcelona"
team2 = "Manchester United"
prompt_start= "The following is a transcription chunk extracted from the commentary of a soccer match between " + team1 + " and " + team2 + ": "
prompt_end="If the chunk includes an event that could be considered an important event, describe it to a soccer fan in an engaging way as if you are the commentator. If not, output ‘N/A’."





while True:
    files = os.listdir(dir_path + '/generated_chunks/transcript_chunks')

    # add all new files and endswith .txt
    added = [f for f in files if f not in allFiles and f.endswith('.txt')]
    # update allFiles with only the files that end with .txt
    allFiles = [f for f in files if f.endswith('.txt')]

    if not added:
        if label:
            print('Waiting for text files...')
        label = False
        time.sleep(1)
    else:
        label = True
        for file in added:
            transcript_file= file
            print('Text file found: ' + transcript_file)
            transcript_path = dir_path + '/generated_chunks/transcript_chunks/' + transcript_file
            with open(transcript_path) as f:
                contents = f.read()
            
            prompt = prompt_start + " " + contents + " "+ prompt_end
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

            response = completion.choices[0].text
            chunkTimeSec = ((CHUNK_NUM+1) * CHUNK_DUR) / 2
            chunkMinutes = int(chunkTimeSec / 60)
            chunkSeconds = chunkTimeSec % 60
            
            my_dict = {
                "minutes": chunkMinutes,
                "seconds": chunkSeconds,
                "highlights": response.lstrip('\n')
            }

            # Convert the dictionary to a JSON object
            json_obj = json.dumps(my_dict)
            headers = {'Content-type': 'application/json'}
            response = requests.post('http://localhost:5000/recieve_higlight', data=json_obj, headers=headers)
     
            # if CHUNK_NUM < 10:
            #     file= open(dir_path + '/generated_chunks/highlight_chunks/highlight_chunk0' + str(CHUNK_NUM) + '.txt', 'w')
            # else:
            #     file= open(dir_path + '/generated_chunks/highlight_chunks/highlight_chunk' + str(CHUNK_NUM) + '.txt', 'w')
            # file.write(json_obj)  #create a text file for each transcription and save in transcript_chunks folder
            # file.close()
            
            CHUNK_NUM+=1


