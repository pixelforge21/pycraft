from flask import Blueprint, render_template, url_for
from datetime import datetime

main_bp = Blueprint("main_bp", __name__, template_folder="../templates", static_folder="../static")

@main_bp.context_processor
def inject_now():
    return {"current_year": datetime.utcnow().year}

@main_bp.route("/")
def home():
    return render_template("home.html")


