import os
from flask import app
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
