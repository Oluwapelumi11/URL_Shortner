from flask import Flask,render_template, request,redirect, url_for,flash,abort, session  
import json, os.path
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key= "rffghjfngejkbnjklenlkenjnjekrnemjnbjk4er"

@app.route("/")
def home():
    return render_template("home.html",keywords=session)

@app.route("/your-url", methods=["GET","POST"])
def your_url():
    url={}
    if request.method == "POST":
        if os.path.exists("urls.json"):
            with open("urls.json") as url_file:
                url = json.load(url_file)

            if request.form["keyword"] in url.keys():
                flash("That keyword has been taken, please use another one")
                return redirect(url_for("home"))

        if "url" in request.form.keys():
            url[request.form["keyword"]] = {"url" : request.form["url"]}
        else:
            f = request.files["file"]
            filename = request.form["keyword"] + secure_filename(f.filename)
            static =  os.path.join(os.getcwd(),"static/")
            f.save(static+filename)
            url[request.form["keyword"]]  = {"file" : filename }

        with open("urls.json","w") as url_file:
            json.dump(url,url_file)
        ##   data ={"name": request.form['keyword'], "time": datetime.now()}
            session[ request.form['keyword']] =  str(datetime.now())
        return render_template("your_url.html",url = request.form["keyword"])
        


    else:
        return redirect(url_for("home"))


@app.route("/<string:keyword>")
def redirect_to_url(keyword):
    if os.path.exists("urls.json"):
        with open("urls.json") as url_file:
            url = json.load(url_file)
        if keyword in url.keys():
            if "url" in url[keyword].keys():
                return redirect(url[keyword]["url"])
            else:
                return redirect(url_for("static", filename=url[keyword]["file"]))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404_page.html"),404
