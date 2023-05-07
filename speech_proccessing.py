import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import time

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
        subscription="balaablue",
        region="THE_ATLANTIC_POLE",
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

    # start recognising
    speech_recognizer.session_started.connect(
        lambda evt: print(f"*****SessionStarted****{evt}*********")
    )

    # stop recognising
    speech_recognizer.session_stopped.connect(
        lambda evt: print("SESSION_STOPPED {}".format(evt))
    )

    results = []

    def handle_results(evt):
        print(evt)
        nonlocal results
        res = {
            "SPOKEN_WORD": evt.result.text,
            "TIME_STAMP": evt.result.offset,
            "DURATION": evt.result.duration,
            "RAW": evt.result,
        }
        if res["SPOKEN_WORD"] != "":
            results.append(res)

    # if it recognise sound then do the call-back
    speech_recognizer.recognized.connect(handle_results)

    # canceled recognising
    speech_recognizer.canceled.connect(lambda evt: print("CANCELLED {}".format(evt)))

    # calling the start recognising func
    result_future = speech_recognizer.start_continuous_recognition_async()
    result_future.get()

    print("____________this happens after 5secs, this print_____________")
    # wait 5sec
    time.sleep(5)

    # calling the stop recognising func
    speech_recognizer.stop_continuous_recognition_async()
    time.sleep(5)
    for items in results:
        print(items["SPOKEN_WORD"])
