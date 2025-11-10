"""
Package: service
Package for the application models and service routes
"""
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config.from_object("service.config")

# Initialize logging
app.logger.setLevel(logging.INFO)
app.logger.info("Setting up an Account Service...")

# Import the models AFTER the Flask app is created
from . import models  # noqa: F401 E402

# Import the routes AFTER the Flask app is created
from . import routes  # noqa: F401 E402

# Import common code
from service.common import cli_commands, error_handlers, log_handlers  # noqa: F401 E402

app.logger.info("Service initialized!")