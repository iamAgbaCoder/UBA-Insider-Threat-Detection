from flask import Flask, render_template

app = Flask(__name__)

# Delay import to avoid circular dependency
from api.file_handler import file_api
from api.chart_handler import chart_api

# Register Blueprint
app.register_blueprint(file_api, url_prefix='/api')
app.register_blueprint(chart_api, url_prefix='/api/results')

# Route to render the upload form
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
