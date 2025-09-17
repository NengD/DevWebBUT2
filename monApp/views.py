from monApp.app import app
import config

@app.route('/')
def index():
    return "Hello world !"

@app.route('/about/')
def about():
    return config.ABOUT


@app.route('/contact/')
def contact():
    return config.CONTACT

if __name__ == "__main__":
    app.run()