from flask import Flask, render_template
from vts import vts
from szyfry import szyfry
import spiewnik


app = Flask(__name__)
spiewnik.setup()


@app.route('/')
def index():
    return render_template("index.html", active_tab="index")

app.register_blueprint(spiewnik.spiewnik, url_prefix="/spiewnik")
        
app.register_blueprint(vts, url_prefix="/vts")

app.register_blueprint(szyfry, url_prefix="/szyfry")

if __name__ == "__main__":
    app.run(debug=True)
    
