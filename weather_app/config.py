import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
env_path = Path('..')/'.env'/'.env'
load_dotenv(dotenv_path=env_path)


SECRET_KEY = os.getenv('SECRET_KEY')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')