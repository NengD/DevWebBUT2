from monApp.app import app
import config
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html",title ="R3.01 Dev Web avec Flask",name="Cricri")

@app.route('/about/')
def about():
    return render_template("about.html",title ="R3.01 Dev Web avec Flask",name="About")


@app.route('/contact/')
def contact():
    return render_template("contact.html",title ="R3.01 Dev Web avec Flask",name="Contact")

if __name__ == "__main__":
    app.run()