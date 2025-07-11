from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env.local')

from constant.server_config import APP_PORT
from server import create_app

app = create_app("development")
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=APP_PORT)
