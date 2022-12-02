from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__, static_folder='staticFiles', template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    email = db.Column(db.String(50))

@app.route("/")
def index():
    dbuser = db.session.query(User).all()
    # print(dbuser)
    for user in dbuser:
        print(user.email)
    return render_template('index.html')

@app.route("/404")
def error404():
    return render_template('404.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('login-form-username')
        password = request.form.get('login-form-password')

        if User.query.filter_by(username = user).filter_by(password = password).first():
            session['username'] = request.form.get('login-form-username')
            return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route("/profile")
def profile():
    if not session.get("username"):
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)