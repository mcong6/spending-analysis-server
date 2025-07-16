import logging

"""Configures the application's logger."""
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
        # You can add other handlers here, like logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)
