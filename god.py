from lib.audio import audio_int, listen_for_speech, save_speech
from lib.stt import detect_intent_audio
import time, os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

def play_clip(filename):
  cmd = 'mplayer -f -really-quiet media/%s.mp4' % filename
  print(cmd)
  os.system(cmd) 


while True:
  filename = listen_for_speech(num_phrases=1)

  start = time.time()
  response = detect_intent_audio('newagent-7404f', int(time.time()), filename, 'de')
  print('response time: %f' % (time.time() - start))

  print(response)

  if response['confidence'] < 0.6:
    play_clip('fallback')
  else:
    play_clip(response['intent'])

  os.remove(filename)
