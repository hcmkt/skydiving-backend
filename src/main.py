import locale

from flask import Flask
from flask_cors import CORS


locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")


from .blueprints.callback import callback
from .blueprints.settings import settings
from .config import Config
from .events import follow, message  # noqa: F401
from .instances.database import init_db
from .instances.scheduler import init_scheduler
from .scheduler import notify  # noqa: F401

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)
init_db(app)
init_scheduler(app)

app.register_blueprint(callback)
app.register_blueprint(settings)
