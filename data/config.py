import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PROVIDER_TOKEN = str(os.getenv("PAYMENTS_PROVIDER_TOKEN"))

admins = [1194575524]

CLIENT_SECRET_FILE = 'google_api'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
folder = '12XGaHoGMiFUqDa3k3rxYasv7G4f-ljEg'