from dotenv import load_dotenv
import os
from datetime import datetime
from speech_proccessing import start_recording


load_dotenv(override=True)

settings = {
    "speechKey": os.environ.get("SPEECH_KEY"),
    "region": os.environ.get("SPEECH_REGION"),
    "language": os.environ.get("SPEECH_LANGUAGE"),
    "openAiKey": os.environ.get("OPENAI_KEY"),
}

output_folder = f'./The_Output_Folder/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
os.makedirs(output_folder)


speech = start_recording()
