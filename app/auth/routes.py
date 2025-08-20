from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .forms import RegisterForm, LoginForm, EnrollmentForm
from ..extensions import db, bcrypt, oauth, login_manager
from ..models import User, Enrollment
from flask_login import login_user, logout_user, login_required, current_user
from ..email_utils import send_enrollment_emails

auth_bp = Blueprint(
    "auth_bp",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# User loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for('main_bp.home'))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Account with that email already exists. Please login.", "warning")
            return redirect(url_for("auth_bp.login"))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created and logged in.", "success")
        return redirect(url_for('main_bp.home'))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/google")
def google_login():
    redirect_uri = url_for("auth_bp.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/google/callback")
def google_callback():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.parse_id_token(token)
    if not userinfo:
        flash("Failed to fetch user info from Google.", "danger")
        return redirect(url_for('auth_bp.login'))

    google_id = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name", email.split("@")[0])

    user = User.query.filter((User.google_id == google_id) | (User.email == email)).first()
    if not user:
        user = User(name=name, email=email, google_id=google_id)
        db.session.add(user)
        db.session.commit()
    else:
        if not user.google_id:
            user.google_id = google_id
            db.session.commit()

    login_user(user)
    flash("Logged in with Google.", "success")
    return redirect(url_for('main_bp.home'))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('main_bp.home'))


@auth_bp.route("/enroll", methods=["GET", "POST"])
@login_required
def enroll():
    """User enrollment (protected route)"""
    form = EnrollmentForm()

    # Prefill form if GET
    if request.method == "GET" and current_user.is_authenticated:
        form.email.data = current_user.email
        form.name.data = current_user.name or ""

    if form.validate_on_submit():
        enrollment = Enrollment(
            user_id=current_user.id,
            name=form.name.data,
            mobile=form.mobile.data,
            student_class=form.student_class.data,
            age=form.age.data,
            email=form.email.data
        )
        db.session.add(enrollment)
        db.session.commit()

        # Send emails (student + admin)
        try:
            send_enrollment_emails(enrollment)
        except Exception as e:
            current_app.logger.error("Email send error: %s", e)

        return render_template("enroll_success.html", enrollment=enrollment)

    return render_template("enroll.html", form=form)


