<img src="https://github.com/jshackles/CloneHeroVideoDownloader/raw/master/assets/icon.png" width="32" height="32"></img> Clone Hero Video Downloader
===========
A simple application that allows you to automatically download the top YouTube video result for songs in your Clone Hero library.

What this does
-------
Clone Hero recognises 'video.mp4' file in every song folder as the video to play in the background of the song chart. 
This program recursively runs through your Clone Hero songs folder to find songs that are missing this video.mp4 file. 

You are given three options for quality:
- 720p (average 5-50MB per video)
- 1080p (100MB+ per video)
- Replace 1080p (deletes every video file you already have and replaces it with 1080p)
  
This will vary greatly depending on specific videos, but generally expect 1080p videos to be at least 2-3x as big.
Options lower than 720p are not included as the quality is so degraded at that stage that it is not really worth even having.

If the file is missing, it then searches YouTube and grabs the first result for that song, using the folder name as the search string. If the download of the first search result fails, it attempts to download the second top result. On
Once downloaded, the file is renamed to 'video.mp4' and placed in the song folder. After this, Clone Hero should automatically recognise the video file and play it during the song.
As YouTube by default does not provide h264 encoded videos above 720p, ffmpeg is used to remux 1080p videos into a format Clone Hero can play.

This program has been tested on very large song libraries with thousands of songs in many nested folders and has been found to be performant.
The amount of time it takes to download videos for all of your songs will be highly dependent on your internet speed.  
A progress bar is provided to indicate how many videos still need to be downloaded and will attempt to estimate the time remaining.

This program has also been designed to run multiple times on the same songs directory. If you add new songs to Clone Hero, simply re-run the program and it will only download the videos that are missing.

Should any songs run into errors, this will be displayed once the program has finished running.

Usage
-------
I found that I needed to downgrade my http client to get this project to work (see requirements.txt). To manage the dependencies, I used `pyenv`.

To create the virtual env:
1. Clone this repository
2. [Install pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
3. Create the virtualenv `pyenv virtualenv clone-hero-video-dl`
4. Activate the environement, you'll need to do this every time you start a new terminal `pyenv activate clone-hero-video-dl`
5. One time install of the project dependencies `pip install -r requirements.txt`
6. Run the thang `python VideoDownload.py`


Notes/FAQ
-------

|WinError2 - File Not Found|  
If you are getting the above issue when using the 1080p option, grab the latest ffmpeg.exe (or equivalent for your platform) executable from this repo and place it in the same folder as your VideoDownload.exe:
https://github.com/BtbN/FFmpeg-Builds/releases  
It will enable the video conversion to work.  

For any songs causing issues, make sure the final folder containing all song files (song.ini etc.) is named 'Artist - song title'. This folder name is where the program gets the artist and song name to search for the video on YouTube.
If you want to replace a video you already have downloaded previously, simply delete or rename the 'video.mp4' file and run the tool again.
