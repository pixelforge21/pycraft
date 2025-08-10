from flask import render_template
from .extensions import mail
from flask_mail import Message
from flask import current_app

def send_enrollment_emails(enrollment):
    """
    Sends two emails:
      1) to the student confirming receipt
      2) to the admin with enrollment details
    enrollment: Enrollment SQLAlchemy object
    """
    try:
        # student email
        student_msg = Message(
            subject="PyCraft — Enrollment Received",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[enrollment.email]
        )
        student_msg.html = render_template("emails/student_received.html", enrollment=enrollment)
        mail.send(student_msg)
    except Exception as e:
        current_app.logger.error("Failed sending email to student: %s", e)

    try:
        # admin email
        admin_msg = Message(
            subject=f"New Enrollment — {enrollment.name}",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[current_app.config.get("ADMIN_EMAIL")]
        )
        admin_msg.html = render_template("emails/admin_notify.html", enrollment=enrollment)
        mail.send(admin_msg)
    except Exception as e:
        current_app.logger.error("Failed sending email to admin: %s", e)
