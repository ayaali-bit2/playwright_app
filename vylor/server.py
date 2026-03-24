from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from vylor.organizations.organizations_routes import organizations_bp
from vylor.invitations import invitations_bp
from vylor.members import members_bp
from vylor.integrations.integrations_routes import integrations_bp
from vylor.authentication.auth_routes import auth_bp
from vylor.callbacks.callbacks_routes import callbacks_bp
from vylor.encryption.encyption_routes import encryption_bp
from vylor.database.postgres_service import PostgresService
from vylor.config import get_config
from vylor.webhooks.webhooks_routes import webhooks_bp
from vylor.feedback.feedback_routes import feedback_bp
from vylor.admin.admin_routes import admin_bp
from vylor.subscriptions.subscriptions_routes import subscription_bp
from vylor.usage.usage_routes import usage_bp
from vylor.chat.chat_routes import chat_bp
from vylor.repo_state.repo_state_routes import repo_state_bp
from .context import GlobalContext
from .dependencies import DependenciesManager
from vylor.services.sentry import get_sentry
from vylor.webhooks.webhook_logs.webhook_logs_service import WebhookLogsService
import logging

load_dotenv()
config = get_config()

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://vylor.ai",
                "https://www.vylor.ai",
                "https://app.vylor.ai",
                "https://staging.vylor.ai",
                "https://www.staging.vylor.ai",
                config.get("frontend", "https://vylor.ai"),
            ]
        }
    },
    supports_credentials=True,
)

# Set up database connection using the singleton PostgresService
service = PostgresService()

# Configure the Flask app with the database connection string
service.configure_app(app)
try:
    WebhookLogsService().delete_old_logs()
except Exception as e:
    logging.error(e)
    get_sentry().capture_exception(e)


@app.before_request
def before_request():
    GlobalContext.initialize_from_flask(DependenciesManager())


@app.teardown_request
def teardown_request(exception=None):
    GlobalContext.clear()


@app.route("/", methods=["GET"])
def root():
    return render_template("landing_page.html"), 200


@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200


# Register blueprints
app.register_blueprint(organizations_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(invitations_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(members_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(integrations_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(auth_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(webhooks_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(callbacks_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(encryption_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(admin_bp, url_prefix="/admin", strict_slashes=False)
app.register_blueprint(feedback_bp, url_prefix="/feedback", strict_slashes=False)
app.register_blueprint(subscription_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(usage_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(chat_bp, url_prefix="", strict_slashes=False)
app.register_blueprint(repo_state_bp, url_prefix="", strict_slashes=False)


def start():
    app.run(host="0.0.0.0", port=80, debug=True)