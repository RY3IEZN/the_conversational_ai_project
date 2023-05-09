from dotenv import load_dotenv
import os
import openai

load_dotenv(override=True)

settings = {
    "openAiKey": os.environ.get("OPENAI_KEY"),
}
