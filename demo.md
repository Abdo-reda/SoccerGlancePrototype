ffmpeg -re -i /home/g05-f22/Downloads/MatchTest.mkv -c:v libx264 -preset veryfast -tune zerolatency -c:a aac -f flv rtmp://localhost:1935/live/mystream

* 4:20 shot on target
* 16:08 penalty 
* 18:30 goal and penalty  <---- start streaming from 17:30>
* 46:20 goal


======= Part 1 =======

--- Intro to Model Server
This is the model server, this page is for clarifaction purposes and not a final product. This is used to show the processing of the stream. The model is server is responsible for processing the stream, dividing into chunks and generating highlights for each chunk then sending those highlights to the api. we will start processing and we will skip ahead some time, we will see some highlights being generated. // to be stored in the database
    //processing could be done automatically. 

--- Intro to API
//Mohamed

======= Part 2 =======

--- Intro to Client application
We will now show an example of how a client would use our API, first the user will register for an account, they would fill their credintial and the target link in which they would receive highlights. After that, the user can go to the dashboard that contains the list of upcoming matching and chose any to register for, once registered, the user will start recieving highlights of the match. 
