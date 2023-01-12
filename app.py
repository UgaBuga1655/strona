from flask import Flask, render_template, request
import vts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/vts')
def vts_route():
    return render_template("vts.html")

@app.route("/vts/file-submit", methods=["POST", "GET"])
def file_submit():
    if request.method == "GET":
        return render_template("file-submit.html")
    if request.method == "POST":
        file = request.form.get('dane')
        try:
            response = vts.main(file)
        except:
            response = ["Niewłaściwy plik"]
        return render_template("file-submit.html", response = response) 


@app.route('/spiewnik')
def spiewnik():
    return render_template("spiewnik.html") 
        

@app.route("/vts/editor")
def editor():
    return render_template("editor.html")

if __name__ == "__main__":
    app.run(debug=True)