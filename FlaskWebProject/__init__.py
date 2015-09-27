"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)


import FlaskWebProject.views
import FlaskWebProject.build_forest as builder

builder.forest()