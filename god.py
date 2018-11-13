from lib.audio import audio_int, listen_for_speech, save_speech
from lib.stt import detect_intent_audio
import time, os, sys
import subprocess, signal

CONFIDENCE_TRESHOLD = 0.6
MPLAYER=['mplayer', '-fs', '-fixed-vo', '-really-quiet']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow.json"

audio_int(150)
if sys.argv[1] == 'test':
    sys.exit(0)

def play_clip(filename):
    cmd = 'mplayer -fs -fixed-vo -really-quiet media/%s.mp4' % filename
    print(cmd)
    os.system(cmd)

def play_loop():
    print("play loop")
    return subprocess.Popen(
        MPLAYER + ['-loop', '0', 'media/loop.mp4'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=False, preexec_fn=os.setsid)

def kill_player(process):
    print("stop loop")
    print(process.pid)
    process.terminate()
    os.system("killall -9 mplayer")
    time.sleep(1)

def kill_subprocesses_and_exit(*args):
    global loop_player
    os.killpg(loop_player.pid, signal.SIGTERM)
    sys.exit(0)

loop_player = play_loop()
signal.signal(signal.SIGINT, kill_subprocesses_and_exit)

while True:
    filename = listen_for_speech(num_phrases=1)
    response = detect_intent_audio('newagent-7404f', int(time.time()), filename, 'de')
    os.remove(filename)

    print(response)
    kill_player(loop_player)
    if response['confidence'] > CONFIDENCE_TRESHOLD \
    or os.path.exists('/media/%s.mp4' % response['intent']):
        play_clip(response['intent'])
    else:
        play_clip('fallback')

    loop_player = play_loop()
