from dotenv import load_dotenv
import os
from datetime import datetime
from speech_proccessing import start_recording, speak
from openai_proccessing import complete_openai


load_dotenv(override=True)

settings = {
    "speechKey": os.environ.get("SPEECH_KEY"),
    "region": os.environ.get("SPEECH_REGION"),
    "language": os.environ.get("SPEECH_LANGUAGE"),
    "openAiKey": os.environ.get("OPENAI_KEY"),
}

output_folder = f'./The_Output_Folder/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
os.makedirs(output_folder)


conversation = []
for i in range(0, 3):
    speech = start_recording()
    conversation.append(speech)
    prompt = ""
    for i in range(len(conversation) - 4, len(conversation)):
        if i >= 0:
            if i % 2 == 0:
                prompt += f"Q: {conversation[i]}\n"
            else:
                prompt += f"A: {conversation[i]}\n"
    prompt += "A: "
    result = complete_openai(prompt=prompt, token=200)
    print(result)
    speak(result, output_folder=output_folder)
    conversation.append(result)
