from flask import Flask, render_template, request
from vts import vts
from szyfry import szyfry


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", active_tab="index")

@app.route('/spiewnik')
def spiewnik():
    return render_template("spiewnik.html", active_tab="spiewnik") 
        
app.register_blueprint(vts, url_prefix="/vts")

app.register_blueprint(szyfry, url_prefix="/szyfry")

if __name__ == "__main__":
    app.run(debug=True)
    
