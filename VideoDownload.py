from codecs import ignore_errors
import configparser
import glob
import os
import time
import yt_dlp
import ffmpeg
from tqdm import tqdm
from youtubesearchpython import VideosSearch

def clean_cookie():
	if os.path.exists(".google-cookie"):
		os.remove(".google-cookie")

def download_video(ydl, url):
	ydl.download([url])
	# Remux video into a format Clone Hero can play
	if (videoQuality != 'mp4'):
		print('Formatting downloaded video for Clone Hero')
		try:
			stream = ffmpeg.input('video.mp4')
			stream = ffmpeg.output(stream, 'output.mp4', vcodec='copy')
			ffmpeg.run(stream, overwrite_output=True, quiet=True)
			os.remove('video.mp4')
			os.rename('output.mp4', 'video.mp4')
		except Exception as e:
			print('Error while converting video. Error: ' + str(e))
		else:
			print('Video ready')

clean_cookie()		

print('Checking for home folder...')
songsFolder = os.path.join(os.getcwd(), "Songs")
time.sleep (0.5)
if os.path.exists(songsFolder):
	print('Songs folder found\n')
	time.sleep (0.5)
	replace = 'false'
	videoQuality = '720p'

	qualityInput = input('Type the number to pick from the following options:\n'
					  + '1. Default quality (720p)\n'
					  + '2. Best quality (1080p, where available; significantly bigger files):\n'
					  + '3. [EXPERIMENTAL] Replace existing videos with 1080p (Caution: Use at your own risk. May malfunction and delete videos)\n\n'
					  + 'Pick between 1-3: ')
	
	if (qualityInput == '1'):
		print('Set to 720p')
		videoQuality = 'mp4'
	elif (qualityInput == '2'):
		print('Set to 1080p. Poor hard drive!')
		videoQuality = 'bestvideo[vcodec^=avc]/best[ext=mp4]/best'
	elif (qualityInput == '3'):
		print('Replacing all videos with 1080p. You have time for a nap!')
		videoQuality = 'bestvideo[vcodec^=avc]/best[ext=mp4]/best'
		replace = 'true'
	else:
		print('You must choose between 1-3. Try again')
		exit()

	homeFolder = os.path.abspath(os.path.join(os.getcwd(), "Songs"))
	os.chdir(homeFolder)
	videoTitle = ''
	i = 0
	erroredSongs = []
	erroredSongNames = []

	for filename in glob.iglob(homeFolder + "/**/song.ini", recursive=True):
		i+=1

	totalcount = i
	
	while True:
		with tqdm(total=i,unit="videos") as pbar:
			for filename in glob.iglob(homeFolder + "/**/song.ini", recursive=True):
				currentSongFileFolder = os.path.dirname(filename)
				currentSongName = os.path.basename(currentSongFileFolder)
				os.chdir(currentSongFileFolder)
				time.sleep (0.0001)
				pbar.update(1)

				if (not os.path.exists("video.mp4") and not currentSongName in erroredSongNames) or replace == 'true':
					try:
						if os.path.exists('video.mp4'):
							os.remove('video.mp4')
							
						# Some song names have strings that will cause YouTube to search for a Clone Hero/Rock Band playthrough video. This strips that out
						titleIssues = ['(2x Bass Pedal Expert+)', '(2x Bass Pedal)', 'RB3', '(RB3 version)', '(Rh)']
						for issue in titleIssues:
							currentSongName = currentSongName.replace(issue, '')

						query = '{} (Official Music Video)'.format(currentSongName)
						print('\nLooking on YouTube for: ' + query)

						# finds the top 2 video URLs from YouTube
						youtube = VideosSearch(query, limit = 2).result()
						url = youtube['result'][0]['link']
						url2 = youtube['result'][1]['link']
						videoTitle = youtube['result'][0]['title']
						print("Search success. Now downloading: " + videoTitle)

						# downloads the song
						ydl_opts = {'outtmpl': 'video.mp4',
								'format': videoQuality,
								'nooverwrites': 0,
								'noplaylist': 1,
								'quiet': True}
						
						with yt_dlp.YoutubeDL(ydl_opts) as ydl:
							try:
								download_video(ydl, url)
							except Exception as e:
								print('Error while downloading: ' + str(e) + '. Trying second video')
								# Try second video if first video errors
								download_video(ydl, url2)
						with open('song.ini') as songCheck:
							# check if the ini file contains unexpected phase shift converter text
							if '//Converted' in songCheck.read():
								erroredSongs.append(filename)
							else:
								# change the song.ini file to attempt to sync the video
								config = configparser.ConfigParser()
								config.read('song.ini')
								# Check uppercase/lowercase config section name
								if config.has_section('song'):
									config.set('song', 'video_start_time', '-3000')
									print('Song ready. Next song...\n')
								elif config.has_section('Song'):
									config.set('Song', 'video_start_time', '-3000')
									print('Song ready. Next song...\n')
								else:
									print('Could not update song.ini. Check the song.ini for potential issues\n')
									erroredSongs.append(filename)
								with open('song.ini', 'w') as configfile:
									config.write(configfile)
						clean_cookie()
					except Exception as e:
						print(e)
						print("Error downloading song: " + currentSongName + ". Skipping")
						erroredSongs.append(videoTitle)
						erroredSongNames.append(currentSongName)
						continue
			else:
				break			
	if erroredSongs:
		print("The following videos were downloaded but not audio-synced")
		for i in erroredSongs:
			print(i, end='\n')
	input("All downloads complete. Checked a total of " + str(totalcount)+ " songs. Press Enter button to exit.")
else:
	input("Did not detect a 'Songs' folder. Check you have placed the .exe file in the directory one level above it. Press any button to exit")
