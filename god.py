from lib.audio import audio_int, listen_for_speech, save_speech
from lib.stt import detect_intent_audio
import time, os
from subprocess import subprocess

CONFIDENCE_TRESHOLD = 0.6
MPLAYER='mplayer -fs -really-quiet'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

def play_clip(filename):
    cmd = '%s media/%s.mp4' % (MPLAYER, filename)
    print(cmd)
    os.system(cmd) 

def play_loop():
    return subprocess.Popen(
        "%s media/loop.mp4" % MPLAYER, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=FALSE, preexec_fn=os.setsid)

def kill_player(process):
    os.killpg(process.pid, signal.SIGTERM)

loop_player = play_loop()

while True:
    filename = listen_for_speech(num_phrases=1)
    response = detect_intent_audio('newagent-7404f', int(time.time()), filename, 'de')
    os.remove(filename)

    print(response)
    kill_loop(loop_player)
    if !os.path.exists('/media/%s.mp4' % response['intent'))
    or response['confidence'] > CONFIDENCE_TRESHOLD:
        play_clip(response['intent'])
    else:
        play_clip('fallback')

    loop_player = play_loop()
