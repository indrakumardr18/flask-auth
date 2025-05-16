from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "indrakumar"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables (run once)
with app.app_context():
    db.create_all()

# Routes

@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already registered")
        
        new_user = User(name=name, email=email, address=address)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['email'] = email
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        session.pop('email', None)
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/book-laundry')
def book_laundry():
    return render_template('book_laundry.html')

@app.route('/orders')
def orders():
    # your code here
    return render_template('orders.html')

@app.route('/support')
def support():
    # Your support page logic here
    return render_template('support.html')



if __name__ == "__main__":
    app.run(debug=True)
