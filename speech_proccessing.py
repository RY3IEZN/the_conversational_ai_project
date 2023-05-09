import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from sounds import play_sound

load_dotenv(override=True)

settings = {
    "speechKey": os.environ.get("SPEECH_KEY"),
    "region": os.environ.get("SPEECH_REGION"),
    "language": os.environ.get("SPEECH_LANGUAGE"),
    "openAiKey": os.environ.get("OPENAI_KEY"),
}


def start_recording():
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(
        subscription="skalmdksmadkmaomdka",
        region="uksouth",
    )
    # speech_config.request_word_level()
    speech_config.set_property(
        property_id=speechsdk.PropertyId.SpeechServiceResponse_OutputFormatOption,
        value="detailed",
    )

    # Creates a speech recognizer using the default microphone (built-in).
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    results = []
    done = False

    def handle_results(evt):
        print(evt)
        nonlocal results
        res = {
            "SPOKEN_WORD": evt.result.text,
            "TIME_STAMP": evt.result.offset,
            "DURATION": evt.result.duration,
            "RAW": evt.result,
        }
        speech_detected()
        print(f"THE-TEXT:{res['SPOKEN_WORD']}")
        if res["SPOKEN_WORD"] != "":
            results.append(res)

    def speech_detected():
        nonlocal last_spoken
        last_spoken = int(datetime.now().timestamp() * 1000)
        print(last_spoken, "last spkemmmmm")

    def speech_canceled(evt):
        nonlocal done
        done = True

    # start recognising
    speech_recognizer.session_started.connect(
        lambda evt: print(f"*****SessionStarted****{evt}*********")
    )

    speech_recognizer.recognizing.connect(lambda evt: speech_detected())

    # stop recognising
    # speech_recognizer.session_stopped.connect(
    #     lambda evt: print("SESSION_STOPPED {}".format(evt))
    # ) --usdd to be this
    speech_recognizer.session_stopped.connect(speech_canceled)

    # canceled recognising
    # speech_recognizer.canceled.connect(lambda evt: print("CANCELLED {}".format(evt))) --used to be this
    speech_recognizer.canceled.connect(speech_canceled)

    # store the raw values in an array
    #

    # if it recognise sound then do the call-back
    speech_recognizer.recognized.connect(handle_results)

    # calling the start recognising func
    result_future = speech_recognizer.start_continuous_recognition_async()
    result_future.get()

    last_spoken = int(datetime.now().timestamp() * 1000)

    play_sound()

    # if not done speaking
    while not done:
        time.sleep(1)
        now = int(datetime.now().timestamp() * 1000)
        inactivity = now - last_spoken
        print(inactivity, "========================")
        if inactivity > 1000:
            play_sound()
        # check if no activity after 3000ms, then call the stop recognising func
        if inactivity > 3000:
            print("stopping_activity_recognitiond")
            speech_recognizer.stop_continuous_recognition_async()
            while not done:
                time.sleep(1)

    output = ""
    for items in results:
        output += items["SPOKEN_WORD"]

    return output
