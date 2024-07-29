"""Flask app creation and configuration"""

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os import getenv
from dotenv import load_dotenv

from .controllers.profile_controller import ProfileController


def create_app() -> Flask:
    """Create flask app and add configurations"""

    load_dotenv()

    app = Flask(__name__)

    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri=getenv("DATABASE_URI"),
        strategy="fixed-window",
        default_limits=["1000 per day", "100 per hour"]
    )

    app.add_url_rule("/api/SteamProfileService/GetRandomProfile", methods=["GET"],
                     view_func=limiter.limit("2 per second")(ProfileController.get_random_profile))
    app.add_url_rule("/api/SteamProfileService/PostSteamID", methods=["POST"],
                     view_func=limiter.limit("3 per minute")(ProfileController.post_steam_id))

    return app
