from flask import Flask
from config import Config
from extensions import db, login_manager
from models import Admin, Opportunity
from routes.auth import auth_bp
from routes.opportunity import opportunity_bp
from flask import send_from_directory

app = Flask(
    __name__,
    static_folder="../sky",   # 👈 IMPORTANT
    static_url_path=""
)
app.config.from_object(Config)


db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(opportunity_bp)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # True only in HTTPS

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))


@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "admin.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)