from lib.audio import audio_int, listen_for_speech, save_speech
from lib.stt import detect_intent_audio
import time, os, sys
import subprocess, signal
import random

INTENT_MEDIA_PATH = 'media'
INTENT_LOOP = 'loop'
INTENT_FALLBACK = 'fallback'
CONFIDENCE_TRESHOLD = 0.6
MPLAYER=['mplayer', '-fs', '-fixed-vo', '-really-quiet']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

audio_int(150)
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    sys.exit(0)

def play_clip(filename):
    cmd = list(MPLAYER).push(filename)
    print(" ".join(cmd))
    os.system(" ".join(cmd))

def play_loop():
    print("play loop")
    if not get_random_intent_media_path(INTENT_LOOP):
        print("loop media not found")
        print("sleeping for 5 seconds")
        time.sleep(5)
        return
    print(get_random_intent_media_path(INTENT_LOOP))
    return subprocess.Popen(
        MPLAYER + ['-loop', '0', get_random_intent_media_path(INTENT_LOOP)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False, preexec_fn=os.setsid)

def kill_player(process):
    print("stop loop")
    try:
        print(process.pid)
        process.terminate()
    except:
        pass
    os.system("killall -9 mplayer")
    time.sleep(1)

def kill_subprocesses_and_exit(*args):
    global loop_player
    os.killpg(loop_player.pid, signal.SIGTERM)
    sys.exit(0)

def get_random_intent_media_path(intent):
    try:
        intent_media_files = os.listdir(os.path.join(INTENT_MEDIA_PATH, intent))
        if len(intent_media_files):
            return os.path.join(INTENT_MEDIA_PATH, intent, random.choice(intent_media_files))
        else:
            return False
    except OSError:
        return False

loop_player = play_loop()
signal.signal(signal.SIGINT, kill_subprocesses_and_exit)

while True:
    filename = listen_for_speech(num_phrases=1)
    response = detect_intent_audio('newagent-7404f', int(time.time()), filename, 'de')
    os.remove(filename)

    print(response)
    kill_player(loop_player)
    if response['confidence'] > CONFIDENCE_TRESHOLD \
    and get_random_intent_media_path(response['intent']):
        play_clip(get_random_intent_media_path(response['intent']))
    else:
        play_clip(get_random_intent_media_path(INTENT_FALLBACK))

    loop_player = play_loop()
