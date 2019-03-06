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
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()
import logging
def log(msg):
    logging.info("{}: {}".format(os.uname()[1], msg))

audio_int(150)
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    sys.exit(0)

def play_clip(filename):
    log("play clip %s" % filename)
    cmd = list(MPLAYER)
    cmd.append(filename)
    cmd = " ".join(cmd)
    os.system(cmd)

def play_loop():
    loop_media = get_random_intent_media_path(INTENT_LOOP)
    if not loop_media:
        print("loop media not found")
        print("sleeping for 5 seconds")
        time.sleep(5)
        return
    log("play loop %s" % loop_media)
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
    os.system("killall -9 mplayer")
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
    log("speech detected")
    response = detect_intent_audio('newagent-7404f', int(time.time()), filename, 'de')
    os.remove(filename)

    log(response)
    kill_player(loop_player)
    if response['confidence'] > CONFIDENCE_TRESHOLD \
    and get_random_intent_media_path(response['intent']):
        play_clip(get_random_intent_media_path(response['intent']))
    else:
        play_clip(get_random_intent_media_path(INTENT_FALLBACK))

    loop_player = play_loop()
