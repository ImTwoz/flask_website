from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='staticFiles', template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/404")
def error404():
    return render_template('404.html')

@app.route("/login")
def login():    
    return render_template('login.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)