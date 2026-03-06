from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

openai_api_key = os.getenv("openai_api_key")
google_api_key = os.getenv("google_api_key")
news_api_key = os.getenv("news_api_key")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")