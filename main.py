import sys
from api_communication import *

# https://www.assemblyai.com/docs <= 참고

filename = sys.argv[1]
audio_url = upload(filename)
save_transcript(audio_url, filename)

# mp4 유튜브의 짧은 영어 영상을 보내면 대본이 많들어지는 마술이..
