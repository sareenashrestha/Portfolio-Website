from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure secret key

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("OUTLOOK_EMAIL")  # Use email from .env
app.config['MAIL_PASSWORD'] = os.getenv("OUTLOOK_APP_PASSWORD")  # Use app password from .env
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("OUTLOOK_EMAIL")  # Set default sender email

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")  # Ensure your main HTML file is named 'index.html'

@app.route("/send-message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Validate form fields
    if not name or not email or not message:
        flash("All fields are required!", "error")
        return render_template("index.html")

    # Send email
    try:
        msg = Message(
            subject=f"Message from {name} via Contact Form",
            recipients=[os.getenv("OUTLOOK_EMAIL")],  # Your email to receive messages
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        )
        mail.connect()  # Ensure connection is established before sending
        mail.send(msg)
        flash("Message sent successfully!", "success")
    except Exception as e:
        flash("An error occurred while sending your message. Please try again later.", "error")
        print(f"Error: {e}")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
