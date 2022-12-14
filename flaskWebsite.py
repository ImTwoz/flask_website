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

class prodIMG(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    img1 = db.Column(db.String)
    img2 = db.Column(db.String)
    img3 = db.Column(db.String)

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)   
    title = db.Column(db.String)
    price = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

@app.route("/")
def index():
    dbuser = db.session.query(User).all()
    for user in dbuser:
        print(user.email)
        
    return render_template('index.html')

@app.route("/404")
@app.errorhandler(404)
def error404(e):
    return render_template('404.html')

@app.route("/auth", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            if request.form.get('login-form-submit'):
                if User.query.filter_by(username = request.form.get('login-form-username')).filter_by(password = request.form.get('login-form-password')).first():
                    session['username'] = request.form.get('login-form-username')
                    return redirect(url_for('profile'))
            elif request.form.get('register-form-submit'):
                if User.query.filter_by(username = request.form.get('register-form-username')).count() < 1 or User.query.filter_by(email = request.form.get('register-form-email')).count() < 1:
                    if request.form.get('register-form-password') != request.form.get('register-form-repassword'):
                        return redirect(url_for('auth'))
                    if '@' not in request.form.get('register-form-email'):
                        return redirect(url_for('auth'))

                    toCommit = User(username = request.form.get('register-form-username'), email = request.form.get('register-form-email'), password = request.form.get('register-form-password'))
                    db.session.add(toCommit)
                    db.session.commit()
                
    return render_template('login-register.html')

@app.route("/profile")
def profile():
    if not session.get("username"):
        return redirect(url_for('login'))

    return render_template('profile.html')

@app.route("/logout")
def logout():
    if not session.get("username"):
        return
    
    session.pop('username')
    return redirect(url_for('login'))

@app.route("/product/<int:id>")
def product(id):
    db.get_or_404(Products, id)
    prodURL = prodIMG.query.filter_by(id = id).first()
    prodPrice = Products.query.filter_by(id = id).first()

    print(prodURL.img1)

    return render_template("shop-single.html", prodURL = prodURL, prodPrice = prodPrice)

@app.route("/cart")
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)