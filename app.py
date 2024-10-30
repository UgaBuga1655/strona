from flask import Flask, render_template
from db_config import db

app = Flask(__name__)
#spiewnik.setup()
from config import Config
app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html", active_tab="index")

from spiewnik import spiewnik
app.register_blueprint(spiewnik, url_prefix="/spiewnik")
        
from vts import vts
app.register_blueprint(vts, url_prefix="/vts")

from szyfry import szyfry
app.register_blueprint(szyfry, url_prefix="/szyfry")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 

    app.run(debug=True)
