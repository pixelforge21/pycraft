import os
from app import create_app

# Create the Flask app using the factory
app = create_app()

if __name__ == "__main__":
    # Local dev server fallback if you run `python run.py`
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)

