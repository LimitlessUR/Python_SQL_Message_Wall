from flask_app import app
import os
from flask_app.controllers import users,messages


if __name__ == "__main__":
    app.run(debug=bool(os.environ.get("DEBUG_STATUS")))