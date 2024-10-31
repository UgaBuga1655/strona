from flask import Flask, render_template
from config import Config, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html", active_tab="index")

from blueprints.spiewnik.routes import spiewnik
app.register_blueprint(spiewnik, url_prefix="/spiewnik")
        
from blueprints.vts.routes import vts
app.register_blueprint(vts, url_prefix="/vts")

from blueprints.szyfry.routes import szyfry
app.register_blueprint(szyfry, url_prefix="/szyfry")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 

    app.run(debug=True)
