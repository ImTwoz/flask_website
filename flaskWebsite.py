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
    for user in dbuser:
        print(user.email)
    return render_template('index.html')

@app.route("/404")
def error404():
    return render_template('404.html')

@app.route("/auth", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            if request.form.get('login-form-submit'):
                if User.query.filter_by(username = request.form.get('login-form-username')).filter_by(password = request.form.get('login-form-password')).first():
                    session['username'] = request.form.get('login-form-username')
                    return redirect(url_for('profile'))
            # elif request.form.get('register-form-submit'):


    return render_template('login-register.html')

@app.route("/profile")
def profile():
    if not session.get("username"):
        return redirect(url_for('/auth'))

    return render_template('profile.html')

@app.route("/logout")
def logout():
    if not session.get("username"):
        return redirect(url_for('login'))
    
    session.pop('username')
    return redirect(url_for('login'))

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)