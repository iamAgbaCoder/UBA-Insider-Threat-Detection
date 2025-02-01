from flask import Blueprint, request, jsonify, render_template
import os

from werkzeug.utils import secure_filename

chart_api = Blueprint("chart_api", __name__)

@chart_api.route("/chart", methods=["GET"])
def chart():
    return render_template('chart.html')
