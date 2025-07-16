from dotenv import load_dotenv

from app.constant.server_config import APP_PORT

load_dotenv(dotenv_path='../.env.local')
from app.server import create_app

app = create_app("development")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=APP_PORT)
