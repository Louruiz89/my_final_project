from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables
import openai

load_dotenv()

my_secret_key = os.getenv("my_openai_key")

openai.api_key = {my_secret_key}