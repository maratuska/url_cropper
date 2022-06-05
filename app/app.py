from app.management import AppManager
from app.settings import conf


app_manager = AppManager(config=conf)
app_instance = app_manager.app_instance
